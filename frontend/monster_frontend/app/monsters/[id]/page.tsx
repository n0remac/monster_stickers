'use client';

import { useGetMonsterByIdQuery } from '@/redux/services/monsterApi';
import { ReactElement } from 'react';
import Image from 'next/image';

const MonsterDetail = ({ params }: { params: { id: string } }): ReactElement | null => {
  const { id } = params;
  const { data: monster, error, isLoading } = useGetMonsterByIdQuery({id: id});
  console.log('monster', monster);
  if (isLoading) return <p>Loading...</p>;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'linear-gradient(to right, #f9f9f9, #e0e0e0)' }}>
      <div style={{ textAlign: 'center', backgroundColor: '#fff', padding: '30px', borderRadius: '10px', boxShadow: '0px 10px 30px rgba(0,0,0,0.15)' }}>
        {monster && 
        <div>
          <h2 style={{ fontSize: '2xl' }}>{monster.element_type} - {monster.creature}</h2>
          <Image src={'http://127.0.0.1:8000'+monster.image_url} alt={monster.creature} width={300} height={300} />
          <p><strong>Type:</strong> {monster.element_type}</p>
          <p><strong>Name:</strong> {monster.creature}</p>
          <p><strong>Description:</strong> {monster.description}</p>
        </div>
        }
      </div>
    </div>
  );
}

export default MonsterDetail;
