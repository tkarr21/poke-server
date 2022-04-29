

import pandas as pd
import random
import math
import json
import os
from collage import collage
from color_poke import coloring_img


class Arceus:

    def __init__(self, distance='euclidean'):
        # all pokemon data
        self.poke = pd.read_csv('Pokemon.csv', header=None, skiprows=1)
        self.poke.columns = field_names = ['name', 'dex', 'type', 'egg_groups', 'color', 'shape',
                                           'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']

        # body template data
        self.body_json = None
        with open('body.json') as f:
            self.body_json = json.load(f)

        self.head_json = None
        self.arm_json = None
        self.leg_json = None
        self.tail_json = None
        with open('attachment.json') as f:
            attachment = json.load(f)
            self.head_json = attachment['head']

        self.type_egg_json = None
        with open('type_egg.json') as f:
            self.type_egg_json = json.load(f)

        self.distance = self.euclidean if distance == 'euclidean' else self.manhattan

    # distance functions
    def euclidean(self, poke1, poke2) -> float:
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        dist = 0
        for stat in stats:

            dist += (poke1[stat] - poke2[stat])**2

        return math.sqrt(dist)

    def manhattan(self, poke1, poke2) -> int:
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        dist = 0
        for stat in stats:

            dist += abs(poke1[stat] - poke2[stat])

        return dist

    def get_poke_type(self, type: str) -> pd.DataFrame:
        # get all pokemon of specified type (includes hybrid typed pokemon)
        return self.poke.loc[self.poke['type'].str.contains(type)]

    def get_poke_egg(self, egg_group: str) -> pd.DataFrame:
        # get all pokemon of specified egg_group
        return self.poke.loc[self.poke['egg_groups'].str.contains(egg_group)]

    def get_dist(self, poke_spec: dict, k: int, poke_to_distance: pd.DataFrame) -> pd.DataFrame:
        dists = []
        for i in range(len(poke_to_distance)):
            dists += [self.distance(poke_to_distance.iloc[i], poke_spec)]

        return poke_to_distance.assign(
            distance=dists).nsmallest(k, columns='distance')

    # Shape and asset selection

    def get_shape(self, neighbors_df):
        # count freq of each shape in nearest neighbors
        shape_freq = {}
        for i, poke in neighbors_df.iterrows():
            if poke['shape'] in shape_freq:
                shape_freq[poke['shape']] += 1
            else:
                shape_freq[poke['shape']] = 1

        # order common neighbors
        ordered = sorted(shape_freq.values(), reverse=True)

        shape = 'upright'

        for k, v in shape_freq.items():
            if v == ordered[0]:
                shape = k

        # FIXME we only support upright and quadruped rn
        # defualting to upright if not quadruped
        if shape != 'quadruped':
            return 'upright'

        return shape

    def sample_freq_dict(self, distrib) -> str:

        marbles = []
        for k, v in distrib.items():
            for i in range(v):
                marbles += [k]

        selection = random.randint(0, len(marbles) - 1)

        return marbles[selection]

    def get_egg_group(self, p_type):

        egg_distrib = self.type_egg_json[p_type]

        return self.sample_freq_dict(egg_distrib)

    def get_head(self, target, egg_group):
        egg_df = self.get_poke_egg(egg_group)

        elected = self.get_dist(target, 1, poke_to_distance=egg_df)
        return int(elected["dex"])

    def get_tail(self, target, egg_group):
        # available tails assets
        tails = [int(x[:-4]) if '-' not in x else int(x[:-6])
                 for x in os.listdir('assets/tail')]
        tails_df = self.poke.loc[self.poke['dex'].isin(tails)]
        tail_egg_df = tails_df.loc[self.poke['egg_groups'].str.contains(
            egg_group)]

        # check if available tails in egg group
        to_distance_df = tails_df if tail_egg_df.empty else tail_egg_df
        elected = self.get_dist(target, 1, poke_to_distance=to_distance_df)

        return int(elected['dex'])

    def select_limb_donor(self, target, egg_group, num_limbs, limb):
        # available arms
        limbs = [x[:-6]
                 for x in os.listdir(f'assets/{limb}') if str(num_limbs) == x[-5]]
        limbs_df = self.poke.loc[self.poke['dex'].isin(
            [int(l) for l in limbs])]
        limbs_egg_df = limbs_df.loc[self.poke['egg_groups'].str.contains(
            egg_group)]

        # check if available arms in egg group
        to_distance_df = limbs_df if limbs_egg_df.empty else limbs_egg_df
        elected = self.get_dist(target, 1, poke_to_distance=to_distance_df)

        return int(elected['dex'])

    def get_appendages(self, target, parts):
        appendages = {}
        anchors = {}

        num_arms = 0
        num_legs = 0
        num_wings = 0
        num_fins = 0

        for part in parts:
            if part == 'head':
                egg_group = self.get_egg_group(target['type'])
                print(f'head egg_group {egg_group}')
                head_donor = self.get_head(target, egg_group)
                appendages[part] = f'assets/head/{head_donor}.png'
                anchors[part] = self.head_json[str(head_donor)]
            if part == 'tail':
                egg_group = self.get_egg_group(target['type'])
                print(f'tail egg_group {egg_group}')
                appendages[part] = f'assets/tail/{self.get_tail(target, egg_group)}.png'
            if 'arm' in part:
                num_arms += 1
            if 'leg' in part:
                num_legs += 1
            if 'wing' in part:
                num_wings += 1
            if 'fin' in part:
                num_fins += 1

        if num_arms:
            egg_group = self.get_egg_group(target['type'])
            print(f'arms egg_group {egg_group}')
            arm_donor = self.select_limb_donor(
                target, egg_group, num_arms, limb='arm')

            count = 1
            for part in parts:
                if 'arm' in part:
                    appendages[part] = f'assets/arm/{arm_donor}-{count}.png'
                    count += 1

        if num_legs:
            egg_group = self.get_egg_group(target['type'])
            print(f'legs egg_group {egg_group}')
            leg_donor = self.select_limb_donor(
                target, egg_group, num_legs, limb='leg')

            # FIXME its gonna put leg-1.png as the back leg if back leg is the
            # first leg entry in the template json
            count = 1
            for part in parts:
                if 'leg' in part:
                    appendages[part] = f'assets/leg/{leg_donor}-{count}.png'
                    count += 1

        if num_wings:
            egg_group = self.get_egg_group(target['type'])
            print(f'wings egg_group {egg_group}')
            wing_donor = self.select_limb_donor(
                target, egg_group, num_wings, limb='wing')

            count = 1
            for part in parts:
                if 'wing' in part:
                    appendages[part] = f'assets/wing/{wing_donor}-{count}.png'
                    count += 1

        if num_fins:
            egg_group = self.get_egg_group(target['type'])
            print(f'fins egg_group {egg_group}')
            fin_donor = self.select_limb_donor(
                target, egg_group, num_fins, limb='fin')

            count = 1
            for part in parts:
                if 'fin' in part:
                    appendages[part] = f'assets/fin/{fin_donor}-{count}.png'
                    count += 1

        return appendages, anchors

    def get_body_template(self, target, shape):
        candidates = None
        if shape == 'upright':
            candidates = self.body_json[shape]
        elif shape == 'quadruped':
            candidates = self.body_json[shape]
        else:
            return

        candidates_df = self.poke.loc[self.poke['dex'].isin(
            [int(c) for c in candidates])]
        elected = self.get_dist(target, 1, poke_to_distance=candidates_df)

        return str(int(elected["dex"]))

    def create_poke(self, target, k):
        typed_distance = self.get_dist(
            target, k, poke_to_distance=self.get_poke_type(target['type']))

        shape = self.get_shape(typed_distance)
        body_template = self.get_body_template(target, shape)

        required_parts = list(self.body_json[shape][body_template].keys())
        appendage_assets, appendage_anchors = self.get_appendages(
            target, required_parts)

        #print(f'assets/body/{body_template}.png')
        #print(json.dumps(appendage_assets, indent=4))

        new_poke = collage(f'assets/body/{body_template}.png',
                           self.body_json[shape][str(body_template)], appendage_assets, appendage_anchors)
        return coloring_img(new_poke, target['type'])


def create(hp, attack, defense, sp_att, sp_def, speed, type):
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    values = [hp, attack, defense, sp_att, sp_def, speed]

    target = {stat: int(values[i]) for i, stat in enumerate(stats)}
    target['type'] = type
    k = 5
    arceus = Arceus()
    return arceus.create_poke(target, k)

def main():
    arceus = Arceus()
    # values = [75, 86, 68, 31, 42, 91]
    # target_type = 'fire'
    # values = [200, 120, 180, 100, 185, 110]
    # target_type = 'electric'
    #values = [10, 150, 25, 154, 20, 50]
    #target_type = 'fire'
    #values = [220, 80, 200, 55, 210, 40]
    #target_type = 'normal'

    # input ranges
    # hp            1 - 255
    # attack        5 - 160
    # defense       5 - 230
    # sp_attack     10 - 154
    # sp_defense    20 - 230
    # speed         5 - 160

    # inputs
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    values = [85, 45, 63, 54, 40, 90]
    target_type = 'electric'

    target = {stat: values[i] for i, stat in enumerate(stats)}
    target['type'] = target_type
    k = 5

    arceus.create_poke(target, k)


if __name__ == '__main__':
    main()
