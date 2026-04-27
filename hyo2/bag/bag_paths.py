import logging
import os.path

from dataclasses import dataclass

from numpy import dtype, uint32, float32, uint16, byte

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class BAGPaths:

    bag_root: str = "BAG_root"
    bag_root_version_tag = "Bag Version"
    bag_default_version_number = b'1.6.3'

    bag_metadata = "BAG_root/metadata"

    bag_elevation = "BAG_root/elevation"
    bag_elevation_min_value_tag = "Minimum Elevation Value"
    bag_elevation_max_value_tag = "Maximum Elevation Value"

    bag_uncertainty = "BAG_root/uncertainty"
    bag_uncertainty_min_value_tag = "Minimum Uncertainty Value"
    bag_uncertainty_max_value_tag = "Maximum Uncertainty Value"
    
    bag_elevation_solution = "BAG_root/elevation_solution"

    bag_tracking_list = "BAG_root/tracking_list"
    bag_tracking_list_len_tag = "Tracking List Length"
    bag_tracking_list_type = dtype([('row', uint32), ('col', uint32),
                                    ('depth', float32), ('uncertainty', float32),
                                    ('track_code', byte), ('list_series', uint16)])

    bag_varres_metadata = "BAG_root/varres_metadata"
    bag_varres_meta_min_dim_x_tag = "min_dimensions_x"
    bag_varres_meta_max_dim_x_tag = "max_dimensions_x"
    bag_varres_meta_min_dim_y_tag = "min_dimensions_y"
    bag_varres_meta_max_dim_y_tag = "max_dimensions_y"
    bag_varres_meta_min_res_x_tag = "min_resolution_x"
    bag_varres_meta_max_res_x_tag = "max_resolution_x"
    bag_varres_meta_min_res_y_tag = "min_resolution_y"
    bag_varres_meta_max_res_y_tag = "max_resolution_y"
    
    bag_varres_refinements = "BAG_root/varres_refinements"
    bag_varres_refs_min_depth_tag = "min_depth"
    bag_varres_refs_max_depth_tag = "max_depth"
    bag_varres_refs_min_uncrt_tag = "min_uncrt"
    bag_varres_refs_max_uncrt_tag = "max_uncrt"
    
    bag_varres_tracking_list = "BAG_root/varres_tracking_list"
    bag_varres_tracking_list_len_tag = "VR Tracking List Length"
    
    @property
    def bag_root_version(self) -> str:
        return os.path.join(self.bag_root, self.bag_root_version_tag)
    
    @property
    def bag_elevation_min_value(self) -> str:
        return os.path.join(self.bag_elevation, self.bag_elevation_min_value_tag)
    
    @property
    def bag_elevation_max_value(self) -> str:
        return os.path.join(self.bag_elevation, self.bag_elevation_max_value_tag)

    @property
    def bag_uncertainty_min_value(self) -> str:
        return os.path.join(self.bag_uncertainty, self.bag_uncertainty_min_value_tag)

    @property
    def bag_uncertainty_max_value(self) -> str:
        return os.path.join(self.bag_uncertainty, self.bag_uncertainty_max_value_tag)

    @property
    def bag_tracking_list_len(self) -> str:
        return os.path.join(self.bag_tracking_list, self.bag_tracking_list_len_tag)

    @property
    def bag_varres_meta_min_dim_x(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_min_dim_x_tag)

    @property
    def bag_varres_meta_max_dim_x(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_max_dim_x_tag)
    
    @property
    def bag_varres_meta_min_dim_y(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_min_dim_y_tag)

    @property
    def bag_varres_meta_max_dim_y(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_max_dim_y_tag)

    @property
    def bag_varres_meta_min_res_x(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_min_res_x_tag)

    @property
    def bag_varres_meta_max_res_x(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_max_res_x_tag)

    @property
    def bag_varres_meta_min_res_y(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_min_res_y_tag)

    @property
    def bag_varres_meta_max_res_y(self) -> str:
        return os.path.join(self.bag_varres_metadata, self.bag_varres_meta_max_res_y_tag)
