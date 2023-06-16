'use client';

import React from 'react';
import { useGetUserMonstersQuery } from '@/redux/services/monsterApi';
import Image from 'next/image';
import { ReactElement } from 'react';
import MonsterDetail from './[id]/page';

const Monsters = (): ReactElement | null => {
  const { isLoading, isFetching, data, error } = useGetUserMonstersQuery(null);

  if (isLoading) return <p>Loading...</p>;
  // if (!userMonsters) return <p>No monsters found</p>;
  if (data !== undefined){
    return (
      <div>
        {data ? (
          <div>
            {data.monsters.map((monster) => (
              <MonsterDetail key={''} params={{id: monster.toString()}} />
            ))}
          </div>
        ) : null}
      </div>
    );
  }
  return null;
}

export default Monsters;
