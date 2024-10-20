magic_mushroom = "magic mushroom", ["max_health", "health", "damage", "damage_multiplier", "range", "speed", "size"], [1, 1, 0.3, 0.5, 5.25, 3, 1], "All stats up!"
sad_onion = "sad onion", ["attack_speed"], [7], "Tears up"
pentagram = "pentagram", ["damage"], [1], "DMG up"
lunch = "lunch", ["max_health", "health"], [1, 1], "HP up"
breakfast = "breakfast", ["max_health", "health"], [1, 1], "HP up"
dinner = "dinner", ["max_health", "health"], [1, 1], "HP up"
halo = "the halo", ["max_health", "health", "damage", "attack_speed", "range", "speed"], [1, 1, 0.3, 2, 0.25, 3], "All stats up"
quarter = "a quarter", ["coins"], [25], "+25 coins"
cat_o_nine_tails = "cat-o-nine-tails", ["damage", "shot_speed"], [1, 0.23], "Shot speed + damage up"
meat = "meat!", ["max_health", "health", "damage"], [1, 1, 0.3], "DMG + HP up"
toothpicks = "toothpicks", ["attack_speed", "shot_speed"], [7, 0.16], "Tears + shot speed up"
stem_cells = "stem cells", ["max_health", "health", "shot_speed"], [1, 1, 0.16], "HP up"
wire_coat_hanger = "wire coat hanger", ["attack_speed"], [7], "Tears up"
roid_rage = "roid rage", ["speed", "range"], [6, 5.25], "Speed and range up"
heart = "<3", ["max_health", "health"], [1, 99], "HP up"
boom = "boom!", ["bombs"], [10], "10 bombs"
dessert = "dessert", ["max_health", "health"], [1, 1], "HP up"
rotten_meat = "rotten meat", ["max_health", "health"], [1, 1], "HP up"
wooden_spoon = "wooden spoon", ["speed"], [3], "Speed up"
the_belt = "the belt", ["speed"], [3], "Speed up"
mom_heels = "mom's heels", ["range"], [5.25], "Range up"
mom_lipstick = "mom's lipstick", ["range"], [5.25], "Range up"
growth_hormones = "growth hormones", ["damage", "speed"], [1, 4], "Speed + DMG up"
bucket_of_lard = "bucket of lard", ["max_health"], [2], "HP up"
speed_ball = "speed ball", ["speed", "shot_speed"], [3, 0.2], "Speed + shot speed up"
synthoil = "synthoil", ["damage", "range"], [1, 5.25], "DMG + range up"
snack = "a snack", ["max_health", "health"], [1, 1], "HP up"

item_list = [
    pentagram, magic_mushroom, sad_onion, lunch, breakfast, 
    dinner, halo, quarter, cat_o_nine_tails, meat, 
    toothpicks, stem_cells, wire_coat_hanger, roid_rage, heart, 
    boom, dessert, rotten_meat, wooden_spoon, the_belt, 
    mom_heels, mom_lipstick, growth_hormones, bucket_of_lard, speed_ball,
    synthoil, snack
    ]

moms_key = "mom's key", ["keys"], [2], "Better chest loot + 2 keys" # doubles the pickups spawn from chests
piggy_bank = "piggy bank", ["coins"], [3], "My life savings" # when taking damage, spawn 1-2 coins
steam_sale = "steam sale", [""], [""], "50% off" # shop prices -50%
bogo_bombs = "bogo bombs", [""], [""], "1+1 BOOM!" # all bomb pickups are now doubled
humbling_bundle = "humbling bundle", [""], [""], "1+1free 4evar!" # doubles the pickups spawn
more_options = "more options", [""], [""], "There are even more options!" # two items now spawn in item rooms, however only one can be taken

shop_items = [more_options, moms_key, piggy_bank, humbling_bundle, steam_sale, bogo_bombs]

heart_container = "heart", ["health"], [1]
key = "key", ["keys"], [1]
bomb = "bomb", ["bombs"], [1]
coin = "coin", ["coins"], [1]

pickup_list = [heart_container, key, bomb, coin]