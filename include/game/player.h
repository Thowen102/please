#pragma once
#include "bn_sprite_ptr.h"
#include "bn_fixed_point.h"
#include "game/types.h"


namespace game {


struct Player {
bn::sprite_ptr spr;
bn::fixed_point vel{0,0};
bool on_ground = false;
int hp = 3;
Ability ability = Ability::None;
int ability_timer = 0;


static Player create(int x, int y);
void update();
void hit();
};


}
