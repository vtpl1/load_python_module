from dataclasses import dataclass
import marshmallow_dataclass


@dataclass
class Element:
    element_id: str
    element_type: str
    config: str


element_schema = marshmallow_dataclass.class_schema(Element)()
