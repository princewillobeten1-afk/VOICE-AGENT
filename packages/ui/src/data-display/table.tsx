"use client";
import * as React from "react";
import { ArrowDownUp } from "lucide-react";
import { Checkbox } from "../forms/selection";
import { SearchInput } from "../forms/input";
import { Button } from "../base/button";

export interface DataTableColumn<T> { key: keyof T; header: string; sortable?: boolean; render?: (row: T) => React.ReactNode; }
export function DataTable<T extends { id: string }>({ data, columns, pageSize = 5, bulkActions }: { data: T[]; columns: DataTableColumn<T>[]; pageSize?: number; bulkActions?: React.ReactNode }) {
  const [query, setQuery] = React.useState("");
  const [page, setPage] = React.useState(1);
  const [sortKey, setSortKey] = React.useState<keyof T | null>(null);
  const [selected, setSelected] = React.useState<string[]>([]);
  const filtered = React.useMemo(() => data.filter((row) => JSON.stringify(row).toLowerCase().includes(query.toLowerCase())), [data, query]);
  const sorted = React.useMemo(() => sortKey ? [...filtered].sort((a, b) => String(a[sortKey]).localeCompare(String(b[sortKey]))) : filtered, [filtered, sortKey]);
  const pages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const visible = sorted.slice((page - 1) * pageSize, page * pageSize);
  const allVisibleSelected = visible.length > 0 && visible.every((row) => selected.includes(row.id));
  return <div className="vs-table-shell"><div className="vs-table-toolbar"><SearchInput placeholder="Search rows" value={query} onChange={(event) => { setQuery(event.target.value); setPage(1); }} />{selected.length ? <div className="vs-bulk-actions"><span>{selected.length} selected</span>{bulkActions}</div> : null}</div><div className="vs-table-wrap"><table className="vs-table"><thead><tr><th><Checkbox checked={allVisibleSelected} onCheckedChange={(checked) => setSelected(checked ? Array.from(new Set([...selected, ...visible.map((row) => row.id)])) : selected.filter((id) => !visible.some((row) => row.id === id)))} aria-label="Select visible rows" /></th>{columns.map((column) => <th key={String(column.key)}>{column.sortable ? <button type="button" onClick={() => setSortKey(column.key)}>{column.header}<ArrowDownUp size={14} /></button> : column.header}</th>)}</tr></thead><tbody>{visible.map((row) => <tr key={row.id} data-selected={selected.includes(row.id)}><td><Checkbox checked={selected.includes(row.id)} onCheckedChange={(checked) => setSelected(checked ? [...selected, row.id] : selected.filter((id) => id !== row.id))} aria-label={`Select row ${row.id}`} /></td>{columns.map((column) => <td key={String(column.key)}>{column.render ? column.render(row) : String(row[column.key])}</td>)}</tr>)}</tbody></table></div><div className="vs-table-footer"><span>{filtered.length} rows</span><div><Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</Button><span>{page} / {pages}</span><Button variant="outline" size="sm" disabled={page >= pages} onClick={() => setPage(page + 1)}>Next</Button></div></div></div>;
}