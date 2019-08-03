from __future__ import unicode_literals

from django.db import models


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
BIGGER = -1
SMALLER = 1
HEROES = {'Y': 'Yallatir', 'W': 'Winter', 'K': 'Kolah', 'A': 'Auriel', 'P': 'The Party'}

class ehEdgePart(models.Model):
    CARDINALITY = (
        (NORTH, "North"),
        (EAST, "East"),
        (SOUTH, "South"),
        (WEST, "West"),
        )
    parent_tile = models.ForeignKey("ehTile", related_name='edges')
    parent_cardinality = models.IntegerField(default=0, choices=CARDINALITY)
    connected_to = models.OneToOneField("ehEdgePart", related_name='connected_from', blank=True, null=True)
    change_size = models.BooleanField(default=False)

    @property
    def yields(self):
        try:
            return self.connected_from
        except:
            return self.connected_to

    @property
    def size_matters(self):
        result = 0
        if self.change_size:
            if hasattr(self,'connected_from'):
                result = BIGGER
            elif self.connected_to:
                result = SMALLER
        return result

    @property
    def through(self):
        result = None
        if self.yields:
            result = self.yields.parent_tile
        return result

    def __unicode__(self):
        p_name = self.parent_tile.id
        return u'Tile {} {}'.format(p_name, self.get_parent_cardinality_display())


class ehTile(models.Model):
    # Tile 59 is the Entrance special tile
    # Tile 60 is the Treasury special tile
    # Tile 61 is the LoopFake non-special tile
    special = models.BooleanField()
    explorer_mark = models.CharField(max_length=1, blank=True, null=True)
    # explorer_enter = models.PositiveIntegerField(blank=True, null=True)
    # explorer_leave = models.PositiveIntegerField(blank=True, null=True)

    @property
    def render_tile(self):
        if self.id == 17:
            tile_contents = 'test'
            # Golems
        elif self.id == 59:
            tile_contents = 'exit'
            # Exit
        elif self.id == 60:
            tile_contents = 'goal'
            # Treasury
        else:
            tile_contents = 'tile'
            # Empty
        hero_explorers = []
        if self.explorers.all():
            for hero in self.explorers.all():
                hero_explorers.append({
                    'symbol': hero.symbol,
                    'name': HEROES[hero.symbol],
                    'size': hero.render_size()
                })
        return {
            'type': tile_contents,
            'people': hero_explorers,
            'explored': self.explorer_mark,
            'navigation': None,
            'id': self.id,
            # 'enter': self.explorer_enter,
            # 'leave': self.explorer_leave,
        }

    @property
    def north(self):
        return self.edge(NORTH)

    @property
    def east(self):
        return self.edge(EAST)

    @property
    def south(self):
        return self.edge(SOUTH)

    @property
    def west(self):
        return self.edge(WEST)

    def edge(self, card):
        return self.edges.filter(parent_cardinality=card).first()

    def __unicode__(self):
        return u'Tile {}'.format(self.id)


class ehExplorer(models.Model):
    location = models.ForeignKey("ehTile", related_name='explorers')
    symbol = models.CharField(max_length=1)
    size = models.PositiveIntegerField(default=1)  # used in the formula size = (2 / (2^x))
    default_size = models.PositiveIntegerField(default=32)  # default point-size for symbol...
    orientation_offset = models.IntegerField(default=0)

    def render_size(self):
        return (self.default_size * (2 / (2**(self.size))))

    def move(self, direction):
        edge_connection = self.location.edge(direction)
        if edge_connection:
            # oldlocation = self.location
            # if oldlocation.explorer_enter == direction:
            #     oldlocation.explorer_enter = None
            # else:
            #     oldlocation.explorer_leave = direction
            # oldlocation.save()
            percieved_arrival_cardinality = ((direction + 2) % 4)
            actual_arrival_cardinality = edge_connection.yields.parent_cardinality
            self.orientation_offset = self.orientation_offset + abs(actual_arrival_cardinality - percieved_arrival_cardinality)
            self.location = edge_connection.through
            self.size += edge_connection.size_matters
            if self.size < 0:
                self.size = 0
            self.save()
            newlocation = self.location
            newlocation.explorer_mark = self.symbol
            # if newlocation.explorer_leave == actual_arrival_cardinality:
            #     newlocation.explorer_leave = None
            # else:
            #     newlocation.explorer_enter = actual_arrival_cardinality
            newlocation.save()

    def look(self):
        '''
        Get visible tiles.
        8 tiles in each cardinal direction
        '''
        if not self.location.special:
            cardinal_array = []
            for start_edge in self.location.edges.all().order_by('parent_cardinality'):
                # Each direction
                hall_array = []
                viewed_tile = self.location
                viewing_cardinality = start_edge.parent_cardinality
                for x in range(8):
                    # unless the tile is special
                    if viewed_tile.special:
                        # if an exit was found, back-fill beyond with empty tiles.
                        viewed_tile = ehTile.objects.get(id=61)
                        viewing_cardinality = 0
                    # Get the edge in the direction we're looking
                    tile_edge = viewed_tile.edge(viewing_cardinality)
                    # Get the connected edge that leads to
                    through_edge = tile_edge.yields
                    # update viewing cardinality to keep looking in a straight line
                    viewing_cardinality = ((through_edge.parent_cardinality + 2) % 4)
                    # update virtual PoV to the viewed tile
                    viewed_tile = through_edge.parent_tile
                    # unless the tile is special and not directly adjacent
                    if viewed_tile.special and x > 0:
                        viewed_tile = ehTile.objects.get(id=61)
                        viewing_cardinality = 0
                    # add viewed tile to hall array
                    hall_array.append(viewed_tile)
                        
                # add hall array to viewer's cardinal array...
                cardinal_array.append(hall_array)
            # cardinal array should now have 8 tiles in each direction, at indices corresponding to the cardinal constants defined above.
            return cardinal_array
        else:
            print "You are not in the Endless Halls."
            return []

    def look_tile_render(self):
        cardinal_array = self.look()
        results = {'North': [], 'East': [], 'South': [], 'West': []}
        percieved_results = []
        for i in range(4):
            shifted_perspective = ((i + self.orientation_offset) % 4)
            percieved_results.append(shifted_perspective)
        results_array = []
        for hall_array in cardinal_array:
            hall_view = []
            for tile_view in hall_array:
                tile_contents = tile_view.render_tile
                # tile_contents['enter'] = ((tile_contents['enter'] + self.orientation_offset) % 4)
                # tile_contents['leave'] = ((tile_contents['leave'] + self.orientation_offset) % 4)
                hall_view.append(tile_contents)
            results_array.append(hall_view)
        results['North'] = results_array[percieved_results[0]]
        results['East'] = results_array[percieved_results[1]]
        results['South'] = results_array[percieved_results[2]]
        results['West'] = results_array[percieved_results[3]]
        return results

    def look_grid_arrange(self):
        default_tile = ehTile.objects.get(id=61)
        filler_render = default_tile.render_tile
        filler_render['shadow'] = True
        look_render = self.look_tile_render()
        south = look_render['South']
        west_reversed = list(reversed(look_render['West']))
        north_reversed = list(reversed(look_render['North']))
        east = look_render['East']
        halls_grid = []
        for x in range(17):
            row_grid = []
            for y in range(17):
                row_grid.append(filler_render)
            halls_grid.append(row_grid)
        # now we have an 11x11 grid of default tiles.
        halls_grid[8][8] = self.location.render_tile
        for i in list(reversed(range(8))):
            halls_grid[i][8] = north_reversed[i]
            halls_grid[8][i+9] = east[i]
        for j in range(8):
            halls_grid[j+9][8] = south[j]
            halls_grid[8][j] = west_reversed[j]
        halls_grid[7][8]['navigation'] = ((NORTH + self.orientation_offset) % 4)
        halls_grid[9][8]['navigation'] = ((SOUTH + self.orientation_offset) % 4)
        halls_grid[8][7]['navigation'] = ((WEST + self.orientation_offset) % 4)
        halls_grid[8][9]['navigation'] = ((EAST + self.orientation_offset) % 4)
        return halls_grid

    def __unicode__(self):
        return u'{}'.format(self.symbol)

