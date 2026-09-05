// Independent decoding/checksum cross-check with MaikelChan/PDSaveEditor.
// Compile alongside that project's unmodified src/Game/SaveData.cpp.
#include "SaveData.h"
#include <array>
#include <cassert>
#include <cstring>
#include <fstream>
#include <iostream>

int main(int argc, char** argv) {
    assert(argc == 2);
    // Upstream editor reads ahead beyond slot/EEPROM boundaries; pad the copy.
    std::array<uint8_t, SAVE_DATA_SIZE + 512> bytes{};
    std::ifstream input(argv[1], std::ios::binary);
    input.read(reinterpret_cast<char*>(bytes.data()), SAVE_DATA_SIZE);
    assert(input.gcount() == SAVE_DATA_SIZE && input.peek() == EOF);
    SaveData data;
    data.Load(bytes.data(), true);
    assert(data.GetGameFileCount() == 1);
    assert(data.GetMultiplayerProfileCount() == 1);
    assert(data.GetMultiplayerSetupCount() == 0);
    auto* game = data.GetGameFile(0);
    assert(game->IsUsed() && game->IsChecksumValid());
    assert(std::strcmp(game->name, "Dark") == 0);
    assert(!game->GetFlag(SinglePlayerFlags::HIRES));
    assert(game->controlModes[0] == 0 && game->controlModes[1] == 0);
    assert(game->sfxVolume == 40 && game->musicVolume == 40 && game->soundMode == 1);
    for (int stage = 0; stage < NUM_SOLOSTAGES; ++stage)
        for (int diff = 0; diff < NUM_DIFFICULTIES; ++diff)
            assert(game->besttimes[stage][diff] > 0);
    const int timedCheats[][3] = {
        {2,0,123}, {5,0,100}, {8,0,230}, {16,2,331}, {12,1,427},
        {9,1,191}, {11,0,170}, {13,2,447}, {14,0,105}, {7,2,479},
        {10,2,235}, {0,1,90}, {1,2,390}, {6,1,300}, {3,1,150},
        {15,1,317}, {4,2,120}
    };
    for (const auto& cheat : timedCheats)
        assert(game->besttimes[cheat[0]][cheat[1]] <= cheat[2]);
    assert(game->thumbnail == 17);
    for (auto challenge : game->mpChallenges) assert(challenge == 15);
    for (auto completion : game->coopcompletions) assert(completion == 0xFFFFF);
    for (int weapon = 0; weapon < 32; ++weapon) assert(game->GetFiringRangeScore(weapon) == 3);
    assert(game->GetFiringRangeScore(32) == 0);
    for (int flag = 0x29; flag <= 0x3A; ++flag)
        assert(game->GetFlag(static_cast<SinglePlayerFlags>(flag)));
    for (int weapon = 0; weapon < 32; ++weapon) assert(game->GetWeaponFound(weapon));
    for (int flag = 0x41; flag <= 0x43; ++flag)
        assert(game->GetFlag(static_cast<SinglePlayerFlags>(flag)));
    auto* mp = data.GetMultiplayerProfile(0);
    assert(mp->IsUsed() && mp->IsChecksumValid());
    assert(std::strcmp(mp->name, "Dark") == 0);
    assert(mp->GetPlayerTitle() == MultiplayerTitles::Perfect);
    for (auto challenge : mp->mpChallenges) assert(challenge == 15);
    auto* boss = data.GetBossFile(0);
    assert(boss->IsUsed() && boss->IsChecksumValid());
    assert(boss->altTitleUnlocked && !boss->altTitleEnabled);
    assert(boss->guid.id == game->pakFileHeader.id);
    assert(boss->guid.deviceSerial == game->pakFileHeader.deviceSerial);
    std::array<uint8_t, SAVE_DATA_SIZE + 512> roundtrip{};
    data.Save(roundtrip.data(), true);
    SaveData reloaded;
    reloaded.Load(roundtrip.data(), true);
    assert(reloaded.GetGameFile(0)->IsChecksumValid());
    assert(reloaded.GetMultiplayerProfile(0)->IsChecksumValid());
    assert(std::strcmp(reloaded.GetGameFile(0)->name, "Dark") == 0);
    std::cout << "PASS: stock N64 EEPROM, Dark solo 63/63, co-op 60/60, gold 32/32, "
                 "challenges 120/120, Dark MP Perfect:1, stock settings, Hi-Res OFF.\n";
}
