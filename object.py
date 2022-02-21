import pygame


class GroupNames:
    object = "object"
    moving_object = "moving_object"
    enemy = "enemy"
    player = "player"
    item = "item"

    @staticmethod
    def list() -> list:
        return ["object", "moving_object", "enemy", "player", "item"]


class Object(object):
    count = 0
    groups = {}

    def __init__(self, screen, image_path: str, position: tuple = (0, 0), angle: float = 0.0, **kwargs):
        self._screen = screen
        self._position = pygame.math.Vector2(position)
        self._angle = angle
        self._image = pygame.image.load(image_path)
        self._image_size = pygame.math.Vector2(self._image.get_size())
        self._corners_offset = []
        # _top_left_corner_offset
        self._corners_offset.append(pygame.math.Vector2((-self._image_size[0]/2, -self._image_size[1]/2)))
        # _bot_left_corner_offset
        self._corners_offset.append(pygame.math.Vector2((-self._image_size[0] / 2, self._image_size[1] / 2)))
        # _bot_right_corner_offset
        self._corners_offset.append(pygame.math.Vector2((self._image_size[0] / 2, self._image_size[1] / 2)))
        # _top_right_corner_offset
        self._corners_offset.append(pygame.math.Vector2((self._image_size[0] / 2, -self._image_size[1] / 2)))
        Object.count += 1
        if GroupNames.object not in Object.groups.keys():
            Object.groups[GroupNames.object] = Group(GroupNames.object)
        Object.groups[GroupNames.object].add(self)

    def __delete__(self):
        Object.count -= 1

    def die(self):
        Object.groups[GroupNames.object].remove(self)
        del self

    @property
    def position(self):
        return tuple(self._position)

    @position.setter
    def position(self, pos: tuple):
        self._position = pygame.Vector2(pos)

    @property
    def angle(self):
        return self._angle

    @property
    def image(self):
        return self._image

    @property
    def image_size(self):
        return self._image_size

    @image.setter
    def image(self, image):
        self._image = image

    def get_corners(self) -> list:
        return [self._position + corner_pos.rotate(self._angle) for corner_pos in self._corners_offset]

    def check_collision(self, other_object) -> bool:
        if self is other_object:
            return False
        self_corners_pos = self.get_corners()
        other_corners_pos = other_object.get_corners()
        for corners_pos in [self_corners_pos, other_corners_pos]:
            # find perpendicular line to edges
            for i in range(2):
                normal = pygame.math.Vector2(corners_pos[i+1].y - corners_pos[i].y, corners_pos[i].x - corners_pos[i+1].x)
                # max_self = min_self = None
                # for corner in self_corners_pos:
                #     projected = normal.x * corner.x + normal.y * corner.y
                #     if min_self is None or projected < min_self:
                #         min_self = projected
                #     if max_self is None or projected > max_self:
                #         max_self = projected
                # max_other = min_other = None
                # for corner in other_corners_pos:
                #     projected = normal.x * corner.x + normal.y * corner.y
                #     if min_other is None or projected < min_other:
                #         min_other = projected
                #     if max_other is None or projected > max_other:
                #         max_other = projected
                # if max_self < min_other or max_other < min_self:
                #     return False
                max_min = [[None, None], [None, None]]  # [[max, min].self, [max, min].other]
                for index, corners in enumerate([self_corners_pos, other_corners_pos]):
                    for corner in corners:
                        projected = normal.x * corner.x + normal.y * corner.y
                        if max_min[index][1] is None or projected < max_min[index][1]:
                            max_min[index][1] = projected
                        if max_min[index][0] is None or projected > max_min[index][0]:
                            max_min[index][0] = projected
                if max_min[0][0] < max_min[1][1] or max_min[1][0] < max_min[0][1]:
                    return False
        return True

    def check_all_collisions(self) -> list:
        return [obj for obj in Object.groups[GroupNames.object] if self.check_collision(obj)]

    def check_group_collisions(self, group) -> list:
        return [obj for obj in group.list if self.check_collision(obj)]

    def draw(self) -> None:
        if self._angle != 0.0:
            self._screen.blit(*self.rotate_image())
        else:
            self._screen.blit(self._image, self._corners_offset[0] + self._position)
        # pygame.draw.circle(self._screen, (0, 255, 0), self._position, 4, 0)
        # pygame.draw.line(self._screen, (0, 255, 0), (self._position[0] - 20, self._position[1]), (self._position[0] + 20, self._position[1]), 2)
        # pygame.draw.line(self._screen, (0, 255, 0), (self._position[0], self._position[1] - 20), (self._position[0], self._position[1] + 20), 2)

    @staticmethod
    def circle_scan_group(group, radius: float, position: tuple) -> list:
        return [obj for obj in group.list if (pygame.Vector2(obj.position) - pygame.Vector2(position)).length() <= radius + obj.image_size[0]]

    @staticmethod
    def draw_all() -> None:
        for obj in Object.groups[GroupNames.object].list:
            obj.draw()

    def rotate_image(self):
        image_center = self._image_size / 2

        # offset from pivot to center
        image_rect = self._image.get_rect(topleft=(self._position[0] - image_center[0], self._position[1] - image_center[1]))
        offset_center_to_pivot = pygame.math.Vector2(self._position) - image_rect.center

        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(self._angle)

        # rotated image center
        rotated_image_center = (self._position[0] - rotated_offset.x, self._position[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(self._image, self._angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return rotated_image, rotated_image_rect


class Group(object):
    def __init__(self, name: str):
        self._name = name
        self._list = []

    @property
    def name(self):
        return self._name

    @property
    def list(self):
        return self._list

    def add(self, obj: Object) -> None:
        if obj not in self._list:
            self._list.append(obj)

    def remove(self, obj: Object) -> None:
        if obj in self._list:
            self._list.remove(obj)

    def clear(self) -> None:
        for obj in self._list:
            self._list.remove(obj)

    def __bool__(self):
        return bool(self._list)

    def __contains__(self, obj: Object):
        return True if obj in self._list else False

    def __len__(self):
        return len(self._list)



