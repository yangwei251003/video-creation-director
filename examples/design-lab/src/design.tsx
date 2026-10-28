import React from 'react';
import {loadFont} from '@remotion/fonts';
import {Easing, interpolate, staticFile} from 'remotion';
// loadFont holds Remotion's render gate until each local font is ready.
void Promise.all([
 loadFont({family:'LabSans',url:staticFile('fonts/NotoSansSC.ttf'),weight:'100 900'}),
 loadFont({family:'LabSerif',url:staticFile('fonts/NotoSerifSC.ttf'),weight:'200 900'}),
]);
export const C={paper:'#F2EDE4',ink:'#202720',red:'#A92F1D',muted:'#5E665E',dark:'#101813',white:'#F1F5EA',lime:'#CEF36F'};
export const progress=(f:number,start:number,end:number)=>interpolate(f,[start,end],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.bezier(.16,1,.3,1)});
export const Label=({children,color=C.muted}:React.PropsWithChildren<{color?:string}>)=><div style={{fontFamily:'LabSans',fontSize:26,letterSpacing:4,color,fontWeight:500}}>{children}</div>;
export const Grain=()=> <svg width="100%" height="100%" style={{position:'absolute',inset:0,pointerEvents:'none',opacity:.055}}><defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".78" numOctaves="3" stitchTiles="stitch" seed="19"/></filter></defs><rect width="100%" height="100%" filter="url(#grain)"/></svg>;
export const Footer=({vertical,dark=false,chapter}:{vertical:boolean;dark?:boolean;chapter:string})=><div style={{position:'absolute',left:vertical?84:110,right:110,bottom:vertical?240:85,display:'flex',justifyContent:'space-between',fontFamily:'LabSans',fontSize:vertical?26:24,letterSpacing:2,color:dark?'#A9B8A6':C.muted,borderTop:`1px solid ${dark?'#455347':'#B7BBAC'}`,paddingTop:20}}><span>视觉叙事 / DESIGN STUDY</span><span>{chapter}</span></div>;
