from ydata.metadata import Metadata
from ydata.utils.data_types import DataType, VariableType
from ydata.dataset.dataset_type import DatasetType

from sdv.metadata.dataset import Metadata as sdvMetadata
from sdv.metadata.table import Table


fabric_to_sdv_types = {
    'int': 'integer'
}

fabric_to_sdv_datatype = {
    'longtext': 'categorical'
}

def fabric_to_sdv_metadata(m: Metadata) -> Table:
    sdv = {"fields": {}}
    for k, v in m.columns.items():
        sdv['fields'][k] = {'type': fabric_to_sdv_datatype.get(v.datatype.value.lower(), v.datatype.value.lower())}
        if v.datatype == DataType.NUMERICAL:
            sdv['fields'][k]['subtype'] = fabric_to_sdv_types.get(v.vartype.value.lower(), v.vartype.value.lower())    
    return Table.from_dict(sdv)