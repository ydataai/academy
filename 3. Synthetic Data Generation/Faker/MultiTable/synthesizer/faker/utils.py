from copy import deepcopy, copy
from sys import stdout
from yaml import safe_dump

import logging
import numpy as np

from ydata.dataset import Dataset, MultiDataset
from ydata.metadata import Metadata
from ydata.metadata.builder import MetadataConfigurationBuilder
from ydata.synthesizers import FakerSynthesizer
from ydata.dataset.schemas.datasets_schema import MultiTableSchema
from ydata.synthesizers.multitable.util import get_table_relationships, topological_sort


logging.basicConfig(
    format="%(levelname)s: %(asctime)s %(message)s",
    level=logging.DEBUG,
    stream=stdout,
)
logger = logging.getLogger("faker_notebook")


def _generate_sample(config, sample_size, locale: str):
    builder = MetadataConfigurationBuilder(config)
    meta = Metadata(configuration_builder=builder)
    synth = FakerSynthesizer(locale=locale)
    synth.fit(meta)
    sample = synth.sample(sample_size)
    return sample


def _get_synthesis_order(schema):
    mt_schema = MultiTableSchema(schema)
    relationships = get_table_relationships(mt_schema)
    digraph = {k: set() for k in schema}
    for child, parent, _ in relationships:
        digraph[parent].add(child)
    order = topological_sort(digraph)
    return order


def _validate_foreign_keys(schema: dict):
    """Checks if all foreign keys definition are valid for the schema.

    Args:
        schema (dict): database schema being built.

    Raises:
        AssertionError: if any foreign key is invalid
    """
    for table in schema:
        table_schema = schema[table]
        foreign_keys = _get_table_fks(table_schema)
        for _, foreign_key in foreign_keys.items():
            parent_table = foreign_key.get("parent_table")
            assert (
                parent_table and parent_table in schema
            ), f"parent_table {parent_table} is invalid"
            parent_column = foreign_key.get("parent_column")
            assert (
                parent_column and parent_column in schema[parent_table]
            ), f"parent_column {parent_column} is invalid"
            assert (
                "primary_key" in schema[parent_table][parent_column]
            ), f"parent_column {parent_table}.{parent_column} is not a PK"
            valid_relation_types = [
                "1-n",
                "1-1",
                "n-n",
                "one-to-one",
                "one-to-many",
                "many-to-many",
            ]
            relation_type = foreign_key.get("relation_type")
            assert (
                relation_type and relation_type in valid_relation_types
            ), f"relation_type {relation_type} is invalid"
            if foreign_key["relation_type"].lower() not in ["1-1", "one-to-one"]:
                assert "min_references" in foreign_key
                assert "max_references" in foreign_key


def _build_database_schema(base_config):
    schema = {k: {"primary_keys": [], "foreign_keys": []} for k in base_config}
    # create primary keys
    for table, config in base_config.items():
        for column in config:
            if "primary_key" in config[column]:
                schema[table]["primary_keys"].append(column)

    # create primary keys
    for table, config in base_config.items():
        for column in config:
            if "foreign_key" in config[column]:
                fk = config[column]["foreign_key"]
                fk_config = {
                    "column": column,
                    "parent_table": fk["parent_table"],
                    "parent_column": fk["parent_column"],
                    "relation_type": fk["relation_type"],
                }
                schema[table]["foreign_keys"].append(fk_config)

    return schema


def _create_pk(table_schema, pk, size):
    column_config = table_schema[pk]
    vartype = column_config["vartype"]
    if vartype.lower() in ["int", "float"]:
        return {
            "datatype": "numerical",
            "vartype": vartype.lower(),
            "min": 1,
            "max": size,  # this will be replaced with the table size
            "unique": True,
        }
    elif vartype.lower() in ["datetime", "date"]:
        assert "min" in column_config
        assert "max" in column_config
        assert "format" in column_config

        return {
            "datatype": "date",
            "vartype": vartype.lower(),
            "min": column_config["min"],
            "max": column_config["max"],
            "format": column_config["format"],
            "unique": True,
        }
    elif vartype.lower() in ["str", "string"]:
        new_config = {
            "datatype": "string",
            "vartype": "string",
            "unique": True,
        }
        if "regex" in column_config:
            new_config["regex"] = column_config["regex"]
        return new_config
    raise ValueError(f"vartype {vartype} not supported")


def _create_one2one_fk_categories(pks):
    categories = {k: 100 / len(pks) for k in pks[:-1]}
    categories[pks[-1]] = 100 - sum(categories.values())
    return categories


def _create_one2many_fk_categories(pks, table_size, min_ref, max_ref):
    n_keys = len(pks)
    base_value = min_ref * n_keys
    if max_ref * n_keys < table_size:
        # if the max references is not enough we need to relax the max references constraint
        max_ref = (table_size // n_keys) + 1
    if base_value > table_size:
        # if there is not enough rows to the min references, ajust it
        min_ref =  table_size // n_keys
        base_value = min_ref * n_keys

    ref_remaining = table_size - base_value
    ref_allocated = 0
    categories = {}

    def get_max(ref_allocated, ref_remaining):
        rest = ref_remaining - ref_allocated
        if rest == 0:
            return min_ref + 1
        elif rest < max_ref:
            return rest + 1
        else:
            return max_ref + 1

    def get_min(ref_allocated, ref_remaining, slots_remaining):
        rest = ref_remaining - ref_allocated
        # max references needs to be allocated to all remaining slots
        if rest / slots_remaining >= max_ref:
            return max_ref

        return min_ref

    for i, k in enumerate(pks[:-1]):
        nrows = np.random.randint(
            get_min(ref_allocated, ref_remaining, n_keys - i),
            get_max(ref_allocated, ref_remaining)
        )
        ref_allocated += nrows - min_ref
        categories[k] = 100 * nrows / table_size

    categories[pks[-1]] = 100 - sum(categories.values())
    return categories


def _create_fk(faker_config, fk, table_size, datasets: dict[str, Dataset]):
    new_config = {}
    parent_table = fk["parent_table"]
    parent_column = fk["parent_column"]
    parent_config = faker_config[parent_table][parent_column]
    new_config["datatype"] = "categorical"
    new_config["vartype"] = parent_config["vartype"]
    pks = datasets[parent_table].value_counts(parent_column).index.tolist()
    if fk["relation_type"].lower() in ["1-1", "one-to-one"]:
        new_config["unique"] = True
        new_config["categories"] = _create_one2one_fk_categories(pks)

    elif fk["relation_type"].lower() in ["1-n", "one-to-many", "n-n", "many-to-many"]:
        fk_config = faker_config[fk["table"]][fk["column"]]["foreign_key"]
        min_ref = fk_config["min_references"]
        max_ref = fk_config["max_references"]

        if max_ref == min_ref:
            new_config["unique"] = False
            new_config["categories"] = _create_one2one_fk_categories(pks)
        else:
            new_config["unique"] = False
            # we use table_size -1 here to avoid a problem with rounding errors
            new_config["categories"] = _create_one2many_fk_categories(
                pks, table_size - 1, min_ref, max_ref
            )
    else:
        raise ValueError(f"relation type {fk['relation_type']} not supported")
    return new_config


def _generate_uniform_probabilities(size):
    prob = [100 / size for _ in range(0, size - 1)]
    prob.append(100 - sum(prob))
    return prob


def _generate_categorical_probabilities(
    distribution: str, cardinality: int, *dist_args, **dist_params
):
    sample_size = cardinality * 100
    if distribution.lower() == "beta":
        dist = np.random.beta(*dist_args, size=sample_size, **dist_params)
    elif distribution.lower() in ["normal", "gaussian"]:
        dist = np.random.normal(*dist_args, size=sample_size, **dist_params)
    else:
        return _generate_uniform_probabilities(cardinality)

    hist, _ = np.histogram(dist, bins=cardinality)
    hist = 100 * hist / sample_size
    hist = [round(h, 8) for h in hist]
    total_prob = round(np.sum(hist), 8)
    if total_prob != 100:
        argmax = np.argmax(hist)
        hist[argmax] += 100 - total_prob
    return hist


def _preprocess_categorical_columns(table_config: dict):
    for col, config in table_config.items():
        categories = config.get("categories")
        distribution = config.get("distribution", "uniform")
        assert distribution.lower() in ["uniform", "gaussian", "normal", "beta"]
        dist_args = config.get("distribution_args", {})
        if categories and (
            isinstance(categories, int) or isinstance(categories, float)
        ):
            categories = list(range(1, categories + 1))

        if categories and isinstance(categories, list):
            if isinstance(dist_args, list):
                probabilities = _generate_categorical_probabilities(
                    distribution, len(categories), *dist_args
                )
            else:
                probabilities = _generate_categorical_probabilities(
                    distribution, len(categories), **dist_args
                )

            table_config[col]["categories"] = {
                k: p for k, p in zip(categories, probabilities)
            }

    return table_config


def get_tables_that_requires_nrows(schema):
    db_schema = _build_database_schema(schema)
    return [
        t for t in db_schema
        if not db_schema[t].get("foreign_keys", [])
    ]


def _get_table_fks(table_schema):
    """Get the configuration of columns defined as foreign keys."""
    return {
        col: config["foreign_key"]
        for col, config in table_schema.items()
        if "foreign_key" in config
    }


def _get_table_size_range(fks, table_sizes):
    """Get the valid range for the table size"""

    def _get_size(fk, limit: str):
        size = table_sizes[fk["parent_table"]]
        if isinstance(size, list):
            size = size[0] if limit == "min" else size[1]
        return size * fk.get(f"{limit}_references", 1)
    if not fks:
        return []
    elif len(fks) == 1:
        fk = list(fks.values())[0]
        min_size = _get_size(fk, "min")
        max_size = _get_size(fk, "max")
    else:
        fks = list(fks.values())
        min_size = _get_size(fks[0], "min")
        max_size = _get_size(fks[0], "max")
        # checks if there is a 1-1 otherwise
        # gets the range of a random parent
        for fk in fks:
            if fk.get("min_references", 1) == 1 and fk.get("max_references", 1) == 1:
                min_size = _get_size(fk, "min")
                max_size = _get_size(fk, "max")
                break

    return [min_size, max_size]


def _get_expected_table_sizes(schema, table_order, table_sizes):
    required_table_sizes = get_tables_that_requires_nrows(schema)
    assert all([t in table_sizes for t in required_table_sizes])
    expected_sizes = copy(table_sizes)
    for t in table_order:
        fks = _get_table_fks(schema[t])
        trange = _get_table_size_range(fks, expected_sizes)
        if t in table_sizes:
            # check if it is in the range
            if not trange or (trange[0] <= table_sizes[t] <= trange[1]):
                expected_sizes[t] = table_sizes[t]
            # if not in range, get the more approximate value in range
            else:
                logger.warning(
                    f"Redefining size for table {t}. "
                    + "Size {expected_sizes[t]} not in range [{trange}]")
                if trange[0] < table_sizes[t]:
                    expected_sizes[t] = trange[0]
                else:
                    expected_sizes[t] = trange[1]
        else:
            expected_sizes[t] = np.random.randint(trange[0], trange[1] + 1)

    return expected_sizes


def _remove_invalid_composite_keys(dataset: Dataset, primary_keys: list[str]) -> Dataset:
    """Remove rows that violate PK unicity constraint."""
    df = dataset.to_dask()
    df = df.drop_duplicates(subset=primary_keys)
    return Dataset(df)


def generate_relational_database(
    schema,
    num_rows_per_table,
    connector,
    locale: str = "en",
    if_exists: str = "replace"
) -> MultiDataset | None:
    _validate_foreign_keys(schema)
    db_schema = _build_database_schema(schema)
    order = _get_synthesis_order(db_schema)
    table_sizes = _get_expected_table_sizes(schema, order, num_rows_per_table)
    faker_config = deepcopy(schema)
    datasets = {}
    for table in order:
        table_config = faker_config[table]
        table_config = _preprocess_categorical_columns(table_config)
        for pk in db_schema[table]["primary_keys"]:
            table_config[pk] = _create_pk(table_config, pk, table_sizes[table])
        for fk in db_schema[table]["foreign_keys"]:
            table_config[fk["column"]] = _create_fk(
                faker_config, fk, table_sizes[table], datasets
            )
        table_data = _generate_sample(
            table_config,
            table_sizes[table],
            locale
        )
        if len(db_schema[table]["primary_keys"]) > 1:
            table_data = _remove_invalid_composite_keys(
                table_data, db_schema[table]["primary_keys"])
        if connector:
            connector.write_table(table_data, name=table, if_exists=if_exists)
            table_data = table_data[db_schema[table]["primary_keys"]]

        datasets[table] = table_data

    if not connector:
        multidataset = MultiDataset(datasets, schema=db_schema)
        return multidataset


def _table_column_to_dict(table_column):
    """Converts a TableColumn to dict."""
    required_blank_msg = "<REQUIRED FIELD>"
    optional_blank_msg = "<OPTIONAL FIELD>"
    datatypes = {
        "int": ["numerical", "categorical"],
        "float": ["numerical", "categorical"],
        "bool": ["categorical"],
        "date": ["date", "categorical"],
        "datetime": ["date", "categorical"],
        "string": ["string", "categorical", "longtext"],
    }
    table_dict = {
        "vartype": str(table_column.variable_type.value)
    }
    if table_column.nullable:
        table_dict["missing"] = f"{optional_blank_msg} - select the % of missing data for nullable column"

    if table_column.primary_key:
        table_dict["primary_key"] = True

    if table_column.is_foreign_key:
        # we expect the fk list to have only one element
        for fk in table_column.foreign_keys:
            parent_table, parent_column = fk.parent.split(".", 1)
            table_dict["foreign_key"] = {
                "parent_table": parent_table,
                "parent_column": parent_column,
                "relation_type": required_blank_msg,
                "min_references": required_blank_msg,
                "max_references": required_blank_msg,
            }
    if "primary_key" not in table_dict and "foreign_key" not in table_dict:
        vartype = table_dict["vartype"]
        table_dict["datatype"] = f"{required_blank_msg} - choose from {datatypes[vartype]}"
    return table_dict


def get_faker_schema_from_connector(connector, output: str = None):
    schema = connector.get_database_schema()
    faker_schema = {}
    for tname, table in schema.tables.items():
        tname = str(tname) 
        faker_schema[tname] = {}
        for column in table.columns:
            faker_schema[tname][str(column.name)] = _table_column_to_dict(column)
    if output:
        with open(output, "w") as file:
            safe_dump(faker_schema, file)
        
    return faker_schema

