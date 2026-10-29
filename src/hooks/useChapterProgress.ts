import { useCallback, useState } from 'react';
const KEY='bones:finished:v1';
function read():number[]{try {const v=JSON.parse(localStorage.getItem(KEY) || '[]');return Array.isArray(v)?v.filter(x=>Number.isInteger(x)):[];}catch{return [];}}
export function useChapterProgress(){
  const [finished,setFinished]=useState<number[]>(read);
  const toggle=useCallback((n:number)=>setFinished(prev=>{const next=prev.includes(n)?prev.filter(v=>v!==n):[...prev,n].sort((a,b)=>a-b);try{localStorage.setItem(KEY,JSON.stringify(next));}catch{/* optional */}return next;}),[]);
  return { finished, toggle };
}
