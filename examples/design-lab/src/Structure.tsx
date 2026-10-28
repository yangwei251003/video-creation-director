import {AbsoluteFill,Freeze,useCurrentFrame,useVideoConfig} from 'remotion';
import {Opening} from './Opening';
import {C,Footer,Grain,Label,progress} from './design';
export const Structure=()=>{
 const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const f=frame/fps,v=height>width;
 const nodes=v?[{x:180,y:760},{x:450,y:1040},{x:720,y:1320}]:[{x:350,y:630},{x:960,y:630},{x:1570,y:630}];
 return <AbsoluteFill style={{background:C.dark,color:C.white,fontFamily:'LabSans',overflow:'hidden'}}>
  <Grain/>
  <div style={{position:'absolute',left:v?84:110,top:v?160:100}}><Label color="#A9B8A6">02 / 空间，让关系更清楚</Label></div>
  <div style={{position:'absolute',left:v?84:110,top:v?350:230,fontSize:v?104:118,lineHeight:1.26,fontWeight:700,fontVariationSettings:`"wght" ${550+200*progress(f,0,.65)}`,translate:`0 ${(1-progress(f,0,.65))*45}px`}}>{v?<>从重点出发，<br/>让关系展开。</>:<>从重点出发，让关系展开。</>}</div>
  <svg width={width} height={height} style={{position:'absolute',inset:0}}>
   <path d={`M ${nodes[0].x} ${nodes[0].y} L ${nodes[1].x} ${nodes[1].y} L ${nodes[2].x} ${nodes[2].y}`} fill="none" stroke="#586C54" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(f,.4,1.4)}/>
   {nodes.map((n,i)=><g key={i} opacity={progress(f,.2+i*.25,.7+i*.25)}><circle cx={n.x} cy={n.y} r={v?70:90} fill={i===1?C.lime:C.dark} stroke={C.lime} strokeWidth="2"/><text x={n.x} y={n.y+15} textAnchor="middle" fill={i===1?C.dark:C.lime} fontSize="42" fontFamily="LabSans" fontWeight="600">{['内容','层级','节奏'][i]}</text></g>)}
  </svg>
  <div style={{position:'absolute',left:v?84:110,top:v?1495:840,fontSize:v?34:36,color:'#A9B8A6',opacity:progress(f,1.4,1.9)}}>{v?<>一条线索连接全片。<br/>每一次运动，都推进理解。</>:<>一条线索连接全片。每一次运动，都推进理解。</>}</div>
  <Footer vertical={v} dark chapter="02 — 03"/>
  {f<.45&&<AbsoluteFill style={{translate:`${-100*progress(f,0,.45)}% 0`}}><Freeze frame={5*fps-1}><Opening/></Freeze></AbsoluteFill>}
 </AbsoluteFill>;
};
