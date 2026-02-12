from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    player_red = models.CharField(max_length=100, default="Player 1 (Red)")
    player_green = models.CharField(max_length=100, default="Player 2 (Green)")
    
    current_turn = models.IntegerField(default=1)
    
    width = models.IntegerField(default=10)
    height = models.IntegerField(default=10)
    
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id} - Turn: {self.current_turn}"

class Node(models.Model):
    """
    Represents a dot occupied by the caterpillar.
    The 'order' field is critical: it turns the dots into a directed graph (path).
    The caterpillar can only be extended from order 0 or the maximum order.
    """
    game = models.ForeignKey(Game, related_name='nodes', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('game', 'x', 'y')
        ordering = ['order']

    def __str__(self):
        return f"({self.x}, {self.y}) - #{self.order}"