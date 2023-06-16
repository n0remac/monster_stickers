import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { UUID } from "crypto";

export type Monster = {
  id: number;
  image_url: string;
  creature: string;
  element_type: string;
  description: string;
//   name: string;
//   email: number;
//   attack: number;
//   health: number;
//   xp: number;
//   max_health: number;
//   max_attack: number;
//   max_xp: number;
//   conscious: boolean;
//   last_battle: string;
};

type Adventure = {
  id: number;
  monster: Monster;
  content: string;
}

type UnregisteredUser = {
  ip: string;
  monsters: UUID[];
}

type Landscape = {
  id: number;
  name: string;
  description: string;
  landscape_type: string;
  feature: string;
  image_url: string;
  monsters: UUID[];

}

interface Movement {
  direction: 'N' | 'S' | 'E' | 'W';
  monster_id: string;
}

export const monsterApi = createApi({
  reducerPath: "MonsterApi",
  refetchOnFocus: true,
  baseQuery: fetchBaseQuery({
    baseUrl: "http://192.168.4.24:8000/",
  }),
  endpoints: (builder) => ({
    getMonsters: builder.query<Monster[], null>({
      query: () => "monsters/",
    }),
    getMonsterById: builder.query<Monster, { id: string }>({
      query: ({ id }) => `monsters/${id}`,
    }),
    getAdventure: builder.query<Adventure, { id: string }>({
      query: ({ id }) =>  `monsters/${id}/adventures/`,
    }),
    getLandscapeById: builder.query<Landscape, { id: string }>({
      query: ({ id }) => `landscape/${id}/`,
    }),
    postMovement: builder.mutation<void, Movement>({
      query: (data) => ({
        url: 'monsters/move/',
        method: 'POST',
        body: { data },
      }),
    }),
    getUserMonsters: builder.query<UnregisteredUser, null>({
      query: () => "monsters/user/",
    }),
    addMonsterToLandscape: builder.mutation<void, { landscape_id: string, monster_id: string }>({
      query: ({ landscape_id, monster_id }) => ({
          url: 'landscape/add_monster/',
          method: 'POST',
          body: { landscape_id, monster_id },
      }),
    }),
    takeMonsterFromLandscape: builder.mutation<void, { landscape_id: string, monster_id: string }>({
      query: ({ landscape_id, monster_id }) => ({
          url: 'landscape/take_monster/',
          method: 'POST',
          body: { landscape_id, monster_id },
      }),
    }),
    getMonsterByIdPost: builder.mutation<Monster, { id: string }>({
      query: ({ id }) => ({
        url: 'api/get_monster/',
        method: 'POST',
        body: { id },
      }),
    }),
    breedMonsters: builder.mutation<Monster, { monster1_id: string, monster2_id: string }>({
      query: ({ monster1_id, monster2_id }) => ({
        url: 'api/breed_monsters/',
        method: 'POST',
        body: { monster1_id, monster2_id },
      }),
    }),
  }),
});

export const {  useGetMonstersQuery, 
                useGetMonsterByIdQuery, 
                useGetAdventureQuery, 
                useGetUserMonstersQuery,
                useGetLandscapeByIdQuery,
                usePostMovementMutation,
                useAddMonsterToLandscapeMutation,
                useGetMonsterByIdPostMutation,
                useTakeMonsterFromLandscapeMutation,
                useBreedMonstersMutation,
            } = monsterApi;
