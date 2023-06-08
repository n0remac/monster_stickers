"use client";

import { useGetMonstersQuery } from "@/redux/services/monsterApi";
import { decrement, increment, reset } from "@/redux/features/counterSlice";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import Image from 'next/image';

export default function Home() {
  const count = useAppSelector((state) => state.counterReducer.value);
  const dispatch = useAppDispatch();

  const { isLoading, isFetching, data, error } = useGetMonstersQuery(null);

  return (
    <main style={{ maxWidth: 1200, marginInline: "auto", padding: 20 }}>
      <div style={{ marginBottom: "4rem", textAlign: "center" }}>
        <h4 style={{ marginBottom: 16 }}>{count}</h4>
        <button onClick={() => dispatch(increment())}>increment</button>
        <button
          onClick={() => dispatch(decrement())}
          style={{ marginInline: 16 }}
        >
          decrement
        </button>
        <button onClick={() => dispatch(reset())}>reset</button>
      </div>

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
          {data.map((monster) => (
            <div
              key={monster.id}
              style={{ border: "1px solid #ccc", textAlign: "center" }}
            >
              <Image
                src={monster.image_url}
                alt={monster.creature}
                width={180}
                height={180}
              />
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
