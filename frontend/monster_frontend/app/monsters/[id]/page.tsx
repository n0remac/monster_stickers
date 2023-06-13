'use client';

import React, { useState } from 'react';
import { useGetMonsterByIdQuery, useGetAdventureQuery } from '@/redux/services/monsterApi';
import Image from 'next/image';

const MonsterDetail = ({ params }: { params: { id: string } }): ReactElement | null => {
  const { id } = params;
  const { data: monster, error: monsterError, isLoading: monsterLoading } = useGetMonsterByIdQuery({id: id});
  const { data: adventure, error: adventureError, isLoading: adventureLoading } = useGetAdventureQuery({id: id});
  const [showAdventure, setShowAdventure] = useState(false);

  console.log('monster', monster);
  if (monsterLoading || adventureLoading) return <p>Loading...</p>;

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-gray-100 to-gray-200">
      <div className="text-center bg-white p-8 rounded shadow-xl">
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
              onClick={() => setShowAdventure(true)}
            >
              Adventure
            </button>
            {showAdventure && adventure &&
              <div>
                <p><strong>Adventure:</strong> {adventure.content}</p>
              </div>
            }
          </div>
        }
      </div>
    </div>
  );
}

export default MonsterDetail;
