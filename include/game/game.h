#pragma once
#include "game/player.h"
#include "game/world.h"
#include "game/ui.h"


namespace game {


struct GameState {
Player player;
World world;
UI ui;
bool paused = false;
int distance = 0; // contributes to score


static GameState start();
bool tick(); // returns false when player dies
};


}
