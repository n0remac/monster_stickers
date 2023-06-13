import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

type Monster = {
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

export const monsterApi = createApi({
  reducerPath: "MonsterApi",
  refetchOnFocus: true,
  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000/",
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
  }),
});

export const { useGetMonstersQuery, useGetMonsterByIdQuery, useGetAdventureQuery } = monsterApi;
