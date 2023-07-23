'use client';

import React, { useState } from 'react';
import { useGetMonsterByIdQuery, useGetAdventureQuery, usePostMovementMutation, useBreedMonstersMutation } from '@/redux/services/monsterApi';
import Image from 'next/image';
import { ReactElement } from 'react';

const MonsterDetail = ({ params }: { params: { id: string } }): ReactElement | null => {
  const { id } = params;
  const { data: monster, error: monsterError, isLoading: monsterLoading } = useGetMonsterByIdQuery({id: id});
  const { data: adventure, error: adventureError, isLoading: adventureLoading } = useGetAdventureQuery({id: id});
  const [postMovement, { isLoading, isError, error }] = usePostMovementMutation()

  const [showAdventure, setShowAdventure] = useState(false);

  const handleClick = async (direction: 'N' | 'S' | 'E' | 'W') => {

    try {
      await postMovement({ direction: direction, monster_id: id});
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex items-center justify-center bg-gradient-to-r from-gray-100 to-gray-200 p-4">
      <div className="text-center bg-white p-8 rounded shadow-xl w-96">
        {monster && 
          <div>
            <h2 className="text-2xl">{monster.element_type} - {monster.creature}</h2>
            <Image 
              src={`http://127.0.0.1:8000${monster.image_url}`} 
              alt={monster.creature} 
              width={300} 
              height={300} 
              className="mx-auto mt-4 mb-4 shadow-md max-w-80"
            />
            <p><strong>Type:</strong> {monster.element_type}</p>
            <p><strong>Name:</strong> {monster.creature}</p>
            <p><strong>Description:</strong> {monster.description}</p>
           
            <button 
              className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              onClick={() => !showAdventure ? setShowAdventure(true): setShowAdventure(false)}
            >
              Adventure
            </button>
            {showAdventure && adventureLoading && <p>Loading...</p>}
            {showAdventure && adventure &&
              <div>
                <p><strong>Adventure:</strong>{adventure.content}</p>
                <div className="mt-4 space-x-4">
                  <button onClick={() => handleClick('N')} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">North</button>
                  <button onClick={() => handleClick('S')} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">South</button>
                  <button onClick={() => handleClick('E')} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">East</button>
                  <button onClick={() => handleClick('W')} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">West</button>
                </div>
              </div>
            }
          </div>
        }
      </div>
    </div>
  );
}

export default MonsterDetail;
