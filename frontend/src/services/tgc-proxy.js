// tgc-proxy.js
// Listens on WebSocket ws://127.0.0.1:13855 and forwards to TGC TCP port 127.0.0.1:13854npm i ws
// npm i ws
// node tgc-proxy.js

import net from 'net';
import WebSocket, { WebSocketServer } from 'ws';

const TGC_HOST = '127.0.0.1';
const TGC_PORT = 13854; // ThinkGear Connector default
const WS_PORT  = 13855; // WebSocket port for Unity WebGL

const wss = new WebSocketServer({ port: WS_PORT }, () =>
  console.log(`TGC proxy listening on ws://127.0.0.1:${WS_PORT}`)
);

wss.on('connection', (ws) => {
  const tcp = net.createConnection({ host: TGC_HOST, port: TGC_PORT }, () =>
    console.log('Connected to ThinkGear TCP')
  );

  tcp.on('data', (chunk) => {
    if (ws.readyState === WebSocket.OPEN) ws.send(chunk);
  });

  tcp.on('error', (err) => {
    console.error('TCP error:', err);
    ws.close();
  });

  tcp.on('close', () => ws.close());

  ws.on('message', (msg) => {
    if (tcp.writable) tcp.write(msg);
  });

  ws.on('close', () => tcp.destroy());
  ws.on('error', (err) => {
    console.error('WS error:', err);
    tcp.destroy();
  });
});

