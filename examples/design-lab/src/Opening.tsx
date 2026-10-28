import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {C,Footer,Grain,Label,progress} from './design';
export const Opening=()=>{
 const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const v=height>width,f=frame/fps;
 const e=progress(f,0,.7),e2=progress(f,.35,1.05),x=v?680:1470,y=v?1160:510,r=v?210:250;
 return <AbsoluteFill style={{background:C.paper,color:C.ink,fontFamily:'LabSans',overflow:'hidden'}}>
  <Grain/>
  <div style={{position:'absolute',left:v?84:110,top:v?160:100}}><Label>01 / 字形，让观点有性格</Label></div>
  <div style={{position:'absolute',left:v?84:110,top:v?390:290,fontFamily:'LabSerif',fontWeight:650,fontSize:v?150:178,lineHeight:1.25,letterSpacing:-5}}>
   <div style={{overflow:'hidden'}}><div style={{translate:`0 ${(1-e)*220}px`}}>让信息</div></div>
   <div style={{overflow:'hidden'}}><div style={{translate:`0 ${(1-e2)*220}px`,color:C.red}}>被看见。</div></div>
   <div style={{height:5,background:C.red,width:(v?610:720)*progress(f,.8,1.5),marginTop:32}}/>
  </div>
  <svg width={width} height={height} style={{position:'absolute',inset:0}}>
   <circle cx={x} cy={y} r={r} fill="none" stroke="#C4C5B7" strokeWidth="1.5"/>
   <circle cx={x} cy={y} r={r*.72} fill="none" stroke={C.red} strokeWidth="2.5" strokeDasharray={`${2*Math.PI*r*.72}`} strokeDashoffset={2*Math.PI*r*.72*(1-progress(f,.6,2.1))} transform={`rotate(-90 ${x} ${y})`}/>
   <line x1={x-r-40} y1={y} x2={x+r+40} y2={y} stroke="#C4C5B7"/>
   <line x1={x} y1={y-r-40} x2={x} y2={y+r+40} stroke="#C4C5B7"/>
   <circle cx={x} cy={y} r={20+22*progress(f,.7,1.5)} fill={C.red}/>
  </svg>
  <div style={{position:'absolute',left:v?84:110,top:v?930:820,fontSize:v?36:35,color:C.muted,opacity:progress(f,1.05,1.5)}}>清楚的重点，值得被好好呈现。</div>
  <Footer vertical={v} chapter="01 — 03"/>
 </AbsoluteFill>;
};
