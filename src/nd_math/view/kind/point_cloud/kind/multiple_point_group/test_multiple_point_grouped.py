from nd_math.view.kind.point_cloud.kind.multiple_point_group.multiple_point_grouped import MultiplePointGrouped
from nd_math.view.kind.point_cloud.point.group.group import Group as PointGroup


class TestMultiplePointGrouped:
    def setup_method(self):
        self._point_group_1 = PointGroup([[4, 5], [6, 7], [10, 12]])
        self._point_group_2 = PointGroup([[5, 6], [7, 8], [9,10]])
        self._point_group_3 = PointGroup([[5, 6], [7, 8], [9,12]])

    def test_simple_render(self):
        point_cloud = MultiplePointGrouped([self._point_group_1, self._point_group_2, self._point_group_3])
        point_cloud.render()

    # def test_with_styled_point_group(self)->None:
    #     color_1 = RgbAlpha(255, 0, 0, 0)
    #     style_1 = Style(color_1)
    #     styled_point_group_1 = Styled(self._point_group_1, style_1)
    #
    #     color_2 = RgbAlpha(0, 255, 0, 0)
    #     style_2 = Style(color_2)
    #     styled_point_group_2 = Styled(self._point_group_2, style_2)
    #
    #     point_cloud = MultiplePointGrouped(PointCloud(styled_point_group_1),[styled_point_group_2])
    #     point_cloud.render()







