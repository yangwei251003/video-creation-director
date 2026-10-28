import {AbsoluteFill,Freeze,useCurrentFrame,useVideoConfig} from 'remotion';
import {Structure} from './Structure';
import {C,Footer,Grain,Label,progress} from './design';
export const Closing=()=>{
 const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const f=frame/fps,v=height>width,e=progress(f,.25,1),size=v?580:650;
 return <AbsoluteFill style={{background:C.paper,color:C.ink,fontFamily:'LabSans',overflow:'hidden'}}>
  <Grain/>
  <div style={{position:'absolute',left:v?84:110,top:v?160:100}}><Label>03 / 运动，让画面有呼吸</Label></div>
  <div style={{position:'absolute',left:v?80:1070,top:v?950:230,width:size,height:size,borderRadius:'50%',border:`2px solid ${C.red}`,scale:.75+.25*e,opacity:e}}>
   {[0,1,2,3].map(i=><div key={i} style={{position:'absolute',inset:45+i*53,border:`1px solid ${i===0?C.red:'#C4C5B7'}`,borderRadius:'50%'}}/>)}
   <div style={{position:'absolute',left:'50%',top:'50%',width:80,height:80,translate:'-50% -50%',borderRadius:'50%',background:C.red}}/>
  </div>
  <div style={{position:'absolute',left:v?84:110,top:v?385:310,fontFamily:'LabSerif',fontSize:v?130:150,lineHeight:1.32,fontWeight:600,letterSpacing:-3,opacity:progress(f,.2,.7),translate:`0 ${(1-e)*55}px`}}>每一帧，<br/><span style={{color:C.red}}>都有理由。</span></div>
  <div style={{position:'absolute',left:v?84:110,top:v?825:775,fontSize:v?36:38,color:C.muted,opacity:progress(f,.85,1.4)}}>字形 · 空间 · 运动</div>
  <Footer vertical={v} chapter="03 — 03"/>
  {f<.5&&<AbsoluteFill style={{clipPath:`circle(${100*(1-progress(f,0,.5))}% at ${v?'67% 69%':'82% 58%'})`}}><Freeze frame={5*fps-1}><Structure/></Freeze></AbsoluteFill>}
 </AbsoluteFill>;
};
