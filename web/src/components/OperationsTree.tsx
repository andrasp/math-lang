import { useState, useMemo } from 'react';
import type { Operation } from '../types';

interface OperationsTreeProps {
  operationsByCategory: Record<string, Operation[]>;
  onInsert?: (text: string) => void;
}

function FolderIcon({ open, className }: { open: boolean; className?: string }) {
  return open ? (
    <svg className={className} width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path
        d="M2 4L4 2H7L8.5 3.5H14L14 4.5L2 4.5V4Z"
        stroke="currentColor"
        strokeWidth="1"
        fill="none"
      />
      <path
        d="M1 5.5H15L13.5 13H2.5L1 5.5Z"
        stroke="currentColor"
        strokeWidth="1"
        fill="currentColor"
        fillOpacity="0.15"
      />
      <line x1="4" y1="8" x2="7" y2="8" stroke="currentColor" strokeWidth="0.75" strokeOpacity="0.5" />
      <line x1="9" y1="10" x2="12" y2="10" stroke="currentColor" strokeWidth="0.75" strokeOpacity="0.5" />
    </svg>
  ) : (
    <svg className={className} width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path
        d="M2 3.5L4 2H7L8.5 3.5H14V12.5H2V3.5Z"
        stroke="currentColor"
        strokeWidth="1"
        fill="currentColor"
        fillOpacity="0.1"
      />
      <path d="M14 3.5L12 3.5L14 5.5V3.5Z" fill="currentColor" fillOpacity="0.3" />
      <circle cx="5" cy="8" r="1" fill="currentColor" fillOpacity="0.4" />
      <line x1="6" y1="8" x2="11" y2="8" stroke="currentColor" strokeWidth="0.5" strokeOpacity="0.3" />
    </svg>
  );
}

function ChevronIcon({ open, className }: { open: boolean; className?: string }) {
  return (
    <svg
      className={`${className} transition-transform duration-150 ${open ? 'rotate-90' : ''}`}
      width="12"
      height="12"
      viewBox="0 0 12 12"
      fill="none"
    >
      <path
        d="M4.5 2.5L8 6L4.5 9.5"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

interface TreeNode {
  name: string;
  path: string;
  children: Map<string, TreeNode>;
  operations: Operation[];
}

function buildTree(operationsByCategory: Record<string, Operation[]>): TreeNode {
  const root: TreeNode = { name: '', path: '', children: new Map(), operations: [] };

  for (const [categoryPath, ops] of Object.entries(operationsByCategory)) {
    const parts = categoryPath.split('/');
    let current = root;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      const path = parts.slice(0, i + 1).join('/');

      if (!current.children.has(part)) {
        current.children.set(part, {
          name: part,
          path,
          children: new Map(),
          operations: [],
        });
      }
      current = current.children.get(part)!;
    }

    current.operations.push(...ops);
  }

  return root;
}

export function OperationsTree({ operationsByCategory, onInsert }: OperationsTreeProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(new Set());

  const filteredByCategory = useMemo(() => {
    if (!searchQuery.trim()) {
      return operationsByCategory;
    }

    const query = searchQuery.toLowerCase();
    const result: Record<string, Operation[]> = {};

    for (const [category, ops] of Object.entries(operationsByCategory)) {
      const filtered = ops.filter(
        (op) =>
          op.identifier.toLowerCase().includes(query) ||
          op.friendly_name.toLowerCase().includes(query) ||
          op.description.toLowerCase().includes(query)
      );
      if (filtered.length > 0) {
        result[category] = filtered;
      }
    }

    return result;
  }, [operationsByCategory, searchQuery]);

  const tree = useMemo(() => buildTree(filteredByCategory), [filteredByCategory]);

  const togglePath = (path: string) => {
    setExpandedPaths((prev) => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };

  const isExpanded = (path: string) => expandedPaths.has(path) || searchQuery.trim() !== '';

  const sortedChildren = Array.from(tree.children.values()).sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return (
    <div className="h-full flex flex-col bg-gray-900 rounded border border-gray-700">
      <div className="px-3 py-2 border-b border-gray-700 bg-gray-800">
        <span className="text-sm font-medium text-gray-300">Operations</span>
      </div>
      <div className="px-2 py-2 border-b border-gray-700">
        <input
          type="text"
          placeholder="Search operations..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-2 py-1 text-sm bg-gray-800 border border-gray-700 rounded text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
      </div>
      <div className="flex-1 overflow-y-auto text-sm">
        {sortedChildren.length === 0 ? (
          <div className="text-gray-500 text-center py-4">No operations found</div>
        ) : (
          sortedChildren.map((node) => (
            <TreeNodeComponent
              key={node.path}
              node={node}
              depth={0}
              isExpanded={isExpanded}
              onToggle={togglePath}
              onInsert={onInsert}
            />
          ))
        )}
      </div>
    </div>
  );
}

interface TreeNodeComponentProps {
  node: TreeNode;
  depth: number;
  isExpanded: (path: string) => boolean;
  onToggle: (path: string) => void;
  onInsert?: (text: string) => void;
}

function TreeNodeComponent({ node, depth, isExpanded, onToggle, onInsert }: TreeNodeComponentProps) {
  const expanded = isExpanded(node.path);
  const hasChildren = node.children.size > 0;
  const hasOperations = node.operations.length > 0;
  const hasContent = hasChildren || hasOperations;
  const totalOps = countOperations(node);

  const sortedChildren = Array.from(node.children.values()).sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return (
    <div>
      <button
        onClick={() => onToggle(node.path)}
        className="w-full flex items-center gap-1.5 px-2 py-1 text-left text-gray-300 hover:bg-gray-800/50 transition-colors duration-100 group"
        style={{ paddingLeft: `${depth * 14 + 8}px` }}
      >
        <span className={`text-gray-500 ${!hasContent ? 'invisible' : ''}`}>
          <ChevronIcon open={expanded} className="w-3 h-3" />
        </span>

        <span className="text-gray-400">
          <FolderIcon open={expanded} className="w-4 h-4" />
        </span>

        <span className="truncate flex-1">
          {node.name} <span className="text-gray-500">({totalOps})</span>
        </span>
      </button>

      {expanded && (
        <>
          {sortedChildren.map((child) => (
            <TreeNodeComponent
              key={child.path}
              node={child}
              depth={depth + 1}
              isExpanded={isExpanded}
              onToggle={onToggle}
              onInsert={onInsert}
            />
          ))}
          {node.operations.map((op) => (
            <OperationItem
              key={op.identifier}
              operation={op}
              depth={depth + 1}
              onInsert={onInsert}
            />
          ))}
        </>
      )}
    </div>
  );
}

function countOperations(node: TreeNode): number {
  let count = node.operations.length;
  for (const child of node.children.values()) {
    count += countOperations(child);
  }
  return count;
}

interface OperationItemProps {
  operation: Operation;
  depth: number;
  onInsert?: (text: string) => void;
}

function isConstant(operation: Operation): boolean {
  return operation.category.startsWith('Constants');
}

function OperationItem({ operation, depth, onInsert }: OperationItemProps) {
  const isConst = isConstant(operation);

  const handleClick = () => {
    if (isConst) {
      onInsert?.(`[[${operation.identifier}]]`);
    } else {
      onInsert?.(`${operation.identifier}()`);
    }
  };

  return (
    <div
      onClick={handleClick}
      className="py-1 cursor-pointer hover:bg-gray-800 group"
      style={{ paddingLeft: `${depth * 12 + 20}px` }}
      title={operation.description}
    >
      <div className="flex items-center gap-1">
        {isConst ? (
          <>
            <span className="text-purple-400">π</span>
            <span className="text-purple-400 font-mono text-xs">[[{operation.identifier}]]</span>
          </>
        ) : (
          <>
            <span className="text-blue-400">ƒ</span>
            <span className="text-blue-400 font-mono text-xs">{operation.identifier}</span>
          </>
        )}
      </div>
      <div className="text-gray-500 text-xs truncate pl-4">{operation.description}</div>
    </div>
  );
}
