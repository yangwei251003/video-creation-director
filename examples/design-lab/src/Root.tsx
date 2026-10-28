import {Composition,Folder,Series,useVideoConfig} from 'remotion';
import {Opening} from './Opening';
import {Structure} from './Structure';
import {Closing} from './Closing';
export const DesignLab=()=>{
 const {fps}=useVideoConfig();
 return <Series>
  <Series.Sequence name="字形" durationInFrames={5*fps} premountFor={fps}><Opening/></Series.Sequence>
  <Series.Sequence name="空间" durationInFrames={5*fps} premountFor={fps}><Structure/></Series.Sequence>
  <Series.Sequence name="运动" durationInFrames={5*fps} premountFor={fps}><Closing/></Series.Sequence>
 </Series>;
};
export const Root=()=> <>
 <Composition id="DesignLabWide" component={DesignLab} width={1920} height={1080} fps={30} durationInFrames={450}/>
 <Composition id="DesignLabVertical" component={DesignLab} width={1080} height={1920} fps={30} durationInFrames={450}/>
 <Folder name="Scenes">
  <Composition id="Typography" component={Opening} width={1920} height={1080} fps={30} durationInFrames={150}/>
  <Composition id="Relations" component={Structure} width={1920} height={1080} fps={30} durationInFrames={150}/>
  <Composition id="Motion" component={Closing} width={1920} height={1080} fps={30} durationInFrames={150}/>
 </Folder>
</>;
