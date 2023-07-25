"use client";

import { useGetMonstersQuery } from "@/redux/services/monsterApi";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import Image from 'next/image';

export default function Home() {
  const count = useAppSelector((state) => state.counterReducer.value);
  const dispatch = useAppDispatch();

  const { isLoading, isFetching, data, error } = useGetMonstersQuery(null);

  return (
    <main style={{ maxWidth: 1200, marginInline: "auto", padding: 20 }}>
      <div>This app is in very early development. Thank you for being an alpha tester. More information and features coming soon!</div>

      {error ? (
        <p>Oh no, there was an error</p>
      ) : isLoading || isFetching ? (
        <p>Loading...</p>
      ) : data ? (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 1fr 1fr",
            gap: 20,
          }}
        >
          <h1>All Monsters</h1>
          {data.map((monster) => (
            <div
              key={monster.id}
              style={{ border: "1px solid #ccc", textAlign: "center" }}
            >
              <Image src={'https://backend:8000'+monster.image_url} alt={monster.creature} width={300} height={300} />
              <h2>{monster.element_type}</h2>
              <h3>{monster.creature}</h3>
              <p>{monster.description}</p>
            </div>
          ))}
        </div>
      ) : null}
    </main>
  );
}
