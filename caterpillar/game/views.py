# caterpillar/game/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Game, Node
from django.views.decorators.csrf import ensure_csrf_cookie
import json

def index(request):
    """Initializes the game board view."""
    game, created = Game.objects.get_or_create(id=1) 
    return render(request, 'game/board.html', {'game': game})

@ensure_csrf_cookie
def make_move(request, game_id):
    """Handles logic for extending the caterpillar line."""
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'GET':
        return JsonResponse({
            'current_turn': game.current_turn,
            'nodes': list(game.nodes.values('x', 'y', 'order'))
        })
    
    data = json.loads(request.body)
    new_x, new_y = int(data.get('x')), int(data.get('y'))
    
    if not game.is_active:
        return JsonResponse({'error': 'Game is over'}, status=400)

    # 1. Is the dot already occupied?
    if Node.objects.filter(game=game, x=new_x, y=new_y).exists():
        return JsonResponse({'error': 'Dot already used'}, status=400)

    nodes = list(game.nodes.all().order_by('order'))
    num_nodes = len(nodes)
    is_valid = False
    new_order = 0
    change_turn = True

    # Adjacency Helper
    def is_adjacent(n1_x, n1_y, n2_x, n2_y):
        return (abs(n1_x - n2_x) == 1 and n1_y == n2_y) or (abs(n1_y - n2_y) == 1 and n1_x == n2_x)

    if num_nodes == 0:
        # Step 1 of Turn 1: Place the very first dot
        is_valid = True
        new_order = 0
        change_turn = False # Still Player 1's turn to pick the second dot
    
    elif num_nodes == 1:
        # Step 2 of Turn 1: Connect the first dot to a second dot
        head = nodes[0]
        if is_adjacent(head.x, head.y, new_x, new_y):
            is_valid = True
            new_order = 1
            change_turn = True # Turn 1 complete, now Player 2
        else:
            return JsonResponse({'error': 'The second dot must be adjacent to the first'}, status=400)

    else:
        # Standard Turn: Connect to either the Head or the Tail
        head, tail = nodes[0], nodes[-1]
        
        if is_adjacent(head.x, head.y, new_x, new_y):
            is_valid = True
            new_order = head.order - 1
            
        elif is_adjacent(tail.x, tail.y, new_x, new_y):
            is_valid = True
            new_order = tail.order + 1
        else:
            return JsonResponse({'error': 'Must connect to one of the ends of the line'}, status=400)

    if is_valid:
        Node.objects.create(game=game, x=new_x, y=new_y, order=new_order)
        # this should fix the turn switching bug where the turn would switch even if the move was invalid -Alex
        if change_turn:
            if game.current_turn == 1:
                game.current_turn = 2
            else:
                game.current_turn = 1
            game.save()
        
        return JsonResponse({
            'success': True, 
            'current_turn': game.current_turn,
            'nodes': list(game.nodes.values('x', 'y', 'order')),
            'is_pending_first_move': (Node.objects.filter(game=game).count() == 1)
        })

    return JsonResponse({'error': 'Invalid move'}, status=400)

def reset_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.nodes.all().delete()
    game.current_turn = 1
    game.save()
    return JsonResponse({'success': True})