#pragma once
#include "bn_vector.h"
#include "bn_sprite_ptr.h"
#include "game/types.h"


namespace game {


struct Platform { bn::sprite_ptr spr; };
struct Enemy { bn::sprite_ptr spr; EnemyKind kind; bn::fixed_point vel{0,0}; int hp=1; };
struct Pickup { bn::sprite_ptr spr; Ability ability; };


struct World {
bn::vector<Platform, 32> platforms;
bn::vector<Enemy, 32> enemies;
bn::vector<Pickup, 16> pickups;
int scroll_x = 0; // world scroll in pixels


void update();
void spawn_chunk(int start_x);
};


}
