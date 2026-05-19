import pygame

class Canvas:
    def __init__(self, width=224, height=288, scale=2):
        self.width = width
        self.height = height
        self.scale = scale
        self.surface = pygame.Surface((width, height))
        
    def clear(self):
        self.surface.fill((0, 0, 0))
        
    def blit(self, source, dest):
        self.surface.blit(source, dest)
        
    def draw_text(self, text, pos, fontsize=10, color="white"):
        # Use a pixel-friendly font if possible, and disable anti-aliasing
        font = pygame.font.SysFont("Pixel", fontsize, bold=True)
        text_surf = font.render(text, False, pygame.Color(color))
        self.surface.blit(text_surf, pos)

    def filled_circle(self, pos, radius, color):
        pygame.draw.circle(self.surface, pygame.Color(color), pos, radius)

    def render_to_screen(self, screen):
        # Scale the virtual surface to the screen size using nearest-neighbor scaling
        scaled_surf = pygame.transform.scale(self.surface, (self.width * self.scale, self.height * self.scale))
        # Note: If pygame.transform.scale is still smooth, we might need to use a different method.
        # But for integer scales, it's often crisp enough.
        screen.surface.blit(scaled_surf, (0, 0))
