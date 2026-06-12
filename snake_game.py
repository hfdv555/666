#!/usr/bin/env python3
"""
Simple Snake Game
A classic snake game that runs on your computer
Controls: Use arrow keys to move the snake
Press SPACE to pause/resume
Press ESC or Q to quit
"""

import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Snake:
    """Snake class to manage snake position and movement"""
    
    def __init__(self):
        # Start in the middle of the grid
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
    
    def move(self):
        """Move the snake in the current direction"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check if head position is valid (not out of bounds or colliding with body)
        if self.is_collision(new_head):
            return False
        
        self.body.insert(0, new_head)
        self.body.pop()
        return True
    
    def is_collision(self, head_pos):
        """Check if the head collides with walls or body"""
        x, y = head_pos
        # Check boundaries
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True
        # Check body collision
        if head_pos in self.body:
            return True
        return False
    
    def grow(self):
        """Make the snake grow by adding a new segment"""
        self.body.append(self.body[-1])
    
    def set_direction(self, direction):
        """Set the direction for the next move (prevent reversing)"""
        # Prevent the snake from reversing into itself
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction

class Food:
    """Food class to manage food position"""
    
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
    
    def generate_position(self, snake_body):
        """Generate a random position that doesn't collide with snake"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                return (x, y)
    
    def respawn(self, snake_body):
        """Respawn food at a new location"""
        self.position = self.generate_position(snake_body)

class SnakeGame:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.paused = False
    
    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction((1, 0))
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Move snake
        if not self.snake.move():
            self.game_over = True
            return
        
        # Check if snake ate food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food.respawn(self.snake.body)
    
    def draw(self):
        """Draw all game elements"""
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw snake
        for i, segment in enumerate(self.snake.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            color = GREEN if i == 0 else (0, 200, 0)  # Head is brighter
            pygame.draw.rect(self.screen, color, (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4))
        
        # Draw food
        food_x = self.food.position[0] * GRID_SIZE
        food_y = self.food.position[1] * GRID_SIZE
        pygame.draw.rect(self.screen, RED, (food_x + 4, food_y + 4, GRID_SIZE - 8, GRID_SIZE - 8))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw pause message
        if self.paused:
            pause_text = self.large_font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 20))
            self.screen.blit(pause_text, text_rect)
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press R to restart or ESC to quit", True, YELLOW)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
