import pygame


class Button:

    def __init__(
        self,
        screen,
        text: str,
        pos: tuple,
        font_size: int = 20,
        colour: str = "black",
        callback=lambda *args: None,
    ) -> None:
        self.screen = screen
        self.x, self.y = pos
        self.colour = colour
        self.font = pygame.font.SysFont('Arial', size=font_size)
        self.callback = callback
        self.change_text(text, colour)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self) -> None:
        self.screen.blit(self.surface, (self.x, self.y))

    def click(self, event, *callback_args) -> None:
        x, y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                self.callback(*callback_args)
