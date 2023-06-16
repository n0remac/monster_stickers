// @ts-nocheck
'use client';

import React, { useEffect, useState } from 'react';

import Image from 'next/image';
import { ReactElement } from 'react';
import { Monster, useAddMonsterToLandscapeMutation, useBreedMonstersMutation, useGetLandscapeByIdQuery, useGetMonsterByIdPostMutation, useGetUserMonstersQuery, useTakeMonsterFromLandscapeMutation } from '@/redux/services/monsterApi';
import { FetchBaseQueryError } from '@reduxjs/toolkit/dist/query';
import { SerializedError } from '@reduxjs/toolkit';

const LandscapeDetail = ({ params }: { params: { id: string } }): ReactElement | null => {
  const { id } = params;
  const { data: landscape, error: landscapeError, isLoading: landscapeLoading } = useGetLandscapeByIdQuery({id: id});
  const { isLoading: userMonstersIsLoading, isFetching: userMonstersIsFetching, data: userMonstersData, error: userMonstersError } = useGetUserMonstersQuery(null);
  const [addMonsterToLandscape, { isLoading: isAddingMonster }] = useAddMonsterToLandscapeMutation();
  const [takeMonsterFromLandscape, { isLoading: isTakingMonster }] = useTakeMonsterFromLandscapeMutation();
  const [getMonsterByIdPost, {isLoading: isLoadingMonser} ] = useGetMonsterByIdPostMutation();
  const [breedMonsters, { isLoading: isBreedingMonster }] = useBreedMonstersMutation();

  const [selectedAdventureMonster, setSelectedAdventureMonster] = useState(null);
  const [selectedBreedMonster, setSelectedBreedMonster] = useState(null);
  const [parentMonster, setParentMonster] = useState(null);
  const [showAdventure, setShowAdventure] = useState(false);
  const [monsterUpdated, setMonsterUpdated] = useState(false);
  const [breed, setBreed] = useState(false);
  const [userMonsterList, setUserMonsterList] = useState<Array<{ data: Monster, error: undefined } | { error: FetchBaseQueryError | SerializedError }>>([]);
  const [landscapeMonsterList, setLandscapeMonsterList] = useState<Array<{ data: Monster, error: undefined } | { error: FetchBaseQueryError | SerializedError }>>([]);


  const sendMonster = async () => {
    if (selectedAdventureMonster) {
      setMonsterUpdated(true);
      await addMonsterToLandscape({ landscape_id: id, monster_id: selectedAdventureMonster });
      setShowAdventure(false);
    }
  }

  const takeMonster = async () => {
    if (selectedAdventureMonster) {
      setLandscapeMonsterList(landscapeMonsterList.filter((monster) => monster.error === undefined &&  monster.data.id !== selectedAdventureMonster));
      await takeMonsterFromLandscape({ landscape_id: id, monster_id: selectedAdventureMonster });
      setShowAdventure(false);
    }
  }

  const breedMonster = async () => {
    if (selectedBreedMonster && parentMonster) {
      await breedMonsters({ monster1_id: selectedBreedMonster, monster2_id: parentMonster });
    }
  }

  useEffect(() => {
    if(userMonstersData && landscape) {
      const get_monsters_by_ids = async (monsters: any, setList: any) => {
        const monster_ids = monsters.map((monster: any) => monster.toString());
        const monster_list = [];
        for (const monster_id of monster_ids) {
          const monster = await getMonsterByIdPost({id: monster_id});
          monster_list.push(monster);
        }
        setList(monster_list);
        setMonsterUpdated(false);
      }
      get_monsters_by_ids(userMonstersData.monsters, setUserMonsterList);
      console.log(landscape);
      if(landscape) get_monsters_by_ids(landscape.monsters, setLandscapeMonsterList);
    }
  }, [userMonstersData, getMonsterByIdPost, landscape, monsterUpdated]);


  return (
    <div className="flex items-center justify-center bg-gradient-to-r from-gray-100 to-gray-200 p-4">
      <div className="text-center w-96">
        <div className='bg-white p-8 rounded shadow-xl '>
          {landscape && 
            <div>
              <h2 className="text-2xl">{landscape.name}</h2>
              <Image 
                src={`http://127.0.0.1:8000${landscape.image_url}`} 
                alt={landscape.name} 
                width={300} 
                height={300} 
                className="mx-auto mt-4 mb-4 shadow-md max-w-80"
              />
              <p><strong>Type:</strong> {landscape.landscape_type}</p>
              <p><strong>Name:</strong> {landscape.name}</p>
              <p><strong>Description:</strong> {landscape.description}</p>
            </div>
          }
          <button 
                className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                onClick={() => !showAdventure ? setShowAdventure(true): setShowAdventure(false)}
              >
                Adventure
          </button>
          {showAdventure &&
            <div>
              <div className='p-2'>
                <select value={selectedAdventureMonster} onChange={(e) => setSelectedAdventureMonster(e.target.value)}>
                  <option value="">Select a monster</option>
                  {userMonsterList && userMonsterList.map(monster => (
                    console.log('id', monster.data.id),
                    <option key={monster.data.id} value={monster.data.id}>{monster.data.creature}</option>
                  ))}
                </select>
                <button className="p-1 m-1 rounded text-white bg-blue-500" onClick={sendMonster} disabled={isAddingMonster}>Send</button>
                <button className="p-1 m-1 rounded text-white bg-blue-500" onClick={takeMonster} disabled={isAddingMonster}>Leave</button>
              </div>
            </div>
          }
        </div>
        <div>
          <h2 className='text-2xl m-5'>Monsters in this area</h2>
            {landscapeMonsterList && landscapeMonsterList.map(monster => (
              <div
                key={monster.data.id}
                className='bg-white p-8 rounded shadow-xl m-2'
              >
                <Image src={'http://127.0.0.1:8000'+monster.data.image_url} alt={monster.data.creature} width={300} height={300} />
                <h2>{monster.data.element_type}</h2>
                <h3>{monster.data.creature}</h3>
                <p>{monster.data.description}</p>
                <button 
                      className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                      onClick={() => !breed ? setBreed(true): setBreed(false)}
                    >
                      Breed
                </button>
                {breed &&
                  <div>
                    <div className='p-2'>
                      <select value={selectedBreedMonster} onChange={(e) => {
                          setParentMonster(monster.data.id);
                          setSelectedBreedMonster(e.target.value)}}>
                        <option value="">Select a monster</option>
                        {landscapeMonsterList && landscapeMonsterList.filter((m) => m.data.id !== monster.data.id).map(breed_monster => (
                            <option key={breed_monster.data.id} value={breed_monster.data.id}>{breed_monster.data.creature}</option>
                        ))}
                      </select>
                      <button className="p-1 m-1 rounded text-white bg-blue-500" onClick={breedMonster} disabled={isAddingMonster}>select</button>
                    </div>
                  </div>
                }  
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}

export default LandscapeDetail;
