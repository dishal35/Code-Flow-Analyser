import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  type Node,
  type Edge,
  ReactFlowProvider,
} from 'react-flow-renderer';
import axios from 'axios';
const GraphPage: React.FC = () => {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);
    const [selectedNodeCode, setSelectedNodeCode] = useState<string>('');
  
    useEffect(() => {
      axios.get('http://localhost:8000/graph-preview')
        .then(res => {
          const { nodes, edges } = res.data;
          setNodes(nodes);
          setEdges(edges);
        })
        .catch(err => {
          console.error('Error fetching graph data:', err);
        });
    }, []);
  
    const onNodeClick = useCallback((_: any, node: Node) => {
      setSelectedNodeCode(node.data?.code || 'No code available');
    }, []);
  
    return (
      <div style={{ display: 'flex', height: '100vh', width: '100vw' }}>
        <div style={{ flex: 3, minWidth: 0, height: '100vh' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodeClick={onNodeClick}
            fitView
          >
            <MiniMap />
            <Controls />
            <Background />
          </ReactFlow>
        </div>

        <div
          style={{
            flex: 1,
            minWidth: 250,
            maxWidth: 350,
            padding: 20,
            borderLeft: '1px solid #ddd',
            background: '#111',
            color: '#fff',
            overflow: 'auto',
          }}
        >
          <h3>Code Snippet</h3>
          <pre>{selectedNodeCode}</pre>
        </div>
      </div>
    );
  };
  
  export default function Wrapped() {
    return (
      <ReactFlowProvider>
        <GraphPage />
      </ReactFlowProvider>
    );
  }
  