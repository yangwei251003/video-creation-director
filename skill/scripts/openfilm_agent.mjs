/** Original background adapter to the installed OpenFilm v0.2.6 AgentSession.
 * Invoke with the installed Electron as Node (launcher: openfilm_agent.py).
 * No foreground input, auth file reads, new credentials, or permission bypass.
 * OpenFilm's internal interface may change: pin and test before upgrading.
 */
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const env=JSON.parse(fs.readFileSync(path.join(dir,'..','local-environment.json'),'utf8')).openfilm;
if(env.version!=='0.2.6')throw new Error('This adapter is validated for OpenFilm 0.2.6 only');
const args=process.argv.slice(2);const option=(name)=>{const n=args.indexOf(name);return n<0?null:args[n+1];};
const project=path.resolve(option('--project')||'.');
if(!fs.existsSync(path.join(project,'film.html')))throw new Error('Choose an existing OpenFilm project');
const module=path.join(path.dirname(env.exe),'resources','app.asar','src','agents.mjs');
const {AgentSession,setChosenPaths}=await import(pathToFileURL(module));
setChosenPaths({codex:env.codex_exe});
const dataDir=env.data_dir||path.join(process.env.APPDATA,'OpenFilm');
const allowed=JSON.parse(fs.readFileSync(path.join(dataDir,'skills.json'),'utf8'));
const updates=[];
const session=new AgentSession({agent:'codex',cwd:project,binDir:path.dirname(env.cli),skills:{dataDir,allowed:allowed.allowed?.codex,mcpAllowed:allowed.mcp?.codex},onUpdate:u=>{updates.push(u);}});
try{
 const info=await session.start();const options=info.configOptions?.find(o=>o.id==='model');
 if(args.includes('--probe')){
  const report={version:env.version,model_options:options,authentication:'session opened; inference not tested'};
  const output=path.join(project,'.film','director-agent');fs.mkdirSync(output,{recursive:true});
  fs.writeFileSync(path.join(output,'probe-'+new Date().toISOString().replace(/[:.]/g,'-')+'.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
 }
 else{
  const promptFile=option('--prompt-file');if(!promptFile)throw new Error('--prompt-file required');
  const model=option('--model')||env.verified_model;
  if(!model||!options?.options?.some(x=>x.value===model))throw new Error('Choose a model actually offered by this session');
  await session.setConfigOption('model',model);
  const prompt=fs.readFileSync(promptFile,'utf8');
  const done=await session.prompt([{type:'text',text:prompt}]);
  const reply=updates.filter(u=>u.sessionUpdate==='agent_message_chunk').map(u=>u.content?.text||'').join('');
  const output=path.join(project,'.film','director-agent');fs.mkdirSync(output,{recursive:true});
  const stamp=new Date().toISOString().replace(/[:.]/g,'-');
  const result={method:'OpenFilm installed AgentSession in background; not a foreground chat UI test',model,sessionId:session.sessionId,done,reply};
  fs.writeFileSync(path.join(output,stamp+'.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({done,model,result:path.join(output,stamp+'.json')}));
 }
}finally{session.close();}
