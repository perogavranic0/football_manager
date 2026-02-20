class Button:
    def __init__(self, x, y, image):
        self.image = image

        # rect samo oko stvarnih (neprozirnih) pixela
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)