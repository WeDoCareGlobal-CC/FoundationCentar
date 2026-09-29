import { db, ws, json, error } from '@appdeploy/sdk';

export type SubscriptionRecord={id:string;entity_type:string;entity_id:string;connection_id:string;created_at:number};
async function listSubscriptions(){const {items}=await db.list<SubscriptionRecord>('entity_subscriptions',{limit:1000});return items;}
export async function removeSubscriptionsByConnection(connectionId:string){const items=await listSubscriptions();const ids=items.filter(i=>i.connection_id===connectionId).map(i=>i.id);if(ids.length)await db.delete('entity_subscriptions',ids);}
export async function addSubscription(entityType:string,entityId:string,connectionId:string){await db.add('entity_subscriptions',[{entity_type:entityType,entity_id:entityId,connection_id:connectionId,created_at:Date.now()}]);}
export async function removeSubscriptions(entityType:string,entityId:string,connectionId:string){const items=await listSubscriptions();const ids=items.filter(i=>i.entity_type===entityType&&i.entity_id===entityId&&i.connection_id===connectionId).map(i=>i.id);if(ids.length)await db.delete('entity_subscriptions',ids);}
export async function notifySubscribers(entityType:string,entityId:string,payload:unknown,excludeConnectionId?:string){const items=await listSubscriptions();const targets=Array.from(new Set(items.filter(i=>i.entity_type===entityType&&i.entity_id===entityId&&i.connection_id!==excludeConnectionId).map(i=>i.connection_id)));if(!targets.length)return;await ws.send(targets,{v:1,type:'entity.update',payload:{entity_type:entityType,entity_id:entityId,data:payload}});}
export const realtimeSubscriptionRoutes={
 'POST /api/subscriptions':[async({body})=>{const b=body as Record<string,string>;if(!b.entity_type||!b.entity_id||!b.connection_id)return error('entity_type, entity_id, connection_id are required');await addSubscription(b.entity_type,b.entity_id,b.connection_id);return json({ok:true});}],
 'POST /api/subscriptions/remove':[async({body})=>{const b=body as Record<string,string>;if(!b.entity_type||!b.entity_id||!b.connection_id)return error('entity_type, entity_id, connection_id are required');await removeSubscriptions(b.entity_type,b.entity_id,b.connection_id);return json({ok:true});}],
};
