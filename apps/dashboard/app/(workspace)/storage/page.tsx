"use client";

import { ArchiveRestore, ArrowDownUp, CheckSquare, Download, FileUp, FolderPlus, Grid2X2, ListFilter, MoreHorizontal, Trash2 } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, IconButton, Progress, SearchInput, Skeleton } from "@voicesense/ui";
import { activity, emptyStorageStates, files, folders, storageStats, uploads } from "../../../lib/storage-data";

export default function StoragePage() {
  const selectedCount = 3;
  const SelectedIcon = files[0].icon;

  return (
    <div className="storage-page">
      <header className="storage-hero">
        <div>
          <p className="ws-kicker">Storage and assets</p>
          <h1>Manage every file, folder, upload, version, and asset lifecycle from one workspace.</h1>
          <p>Browse business assets, stage uploads, inspect metadata, and keep provider-backed storage organized without mixing in AI indexing or processing.</p>
        </div>
        <div className="storage-actions"><Button><FileUp size={16} />Upload</Button><Button variant="outline"><FolderPlus size={16} />New folder</Button></div>
      </header>

      <section className="storage-stat-grid" aria-label="Storage summary">
        {storageStats.map((stat) => <article className={`storage-card storage-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}
      </section>

      <section className="storage-toolbar" aria-label="File controls">
        <div className="storage-breadcrumbs"><span>Acme Co</span><span>/</span><span>Storage</span><span>/</span><strong>Knowledge sources</strong></div>
        <div className="storage-toolbar-actions"><SearchInput placeholder="Search files and folders" /><Button variant="outline" size="sm"><ListFilter size={15} />Filter</Button><Button variant="outline" size="sm"><ArrowDownUp size={15} />Sort</Button><IconButton variant="outline" aria-label="Grid view"><Grid2X2 size={16} /></IconButton></div>
      </section>

      <section className="storage-main-grid">
        <div className="storage-left-stack">
          <article className="storage-upload-zone" aria-label="Upload files"><FileUp size={28} /><div><strong>Drop files or folders to upload</strong><p>Supports documents, PDFs, images, audio, archives, exports, and reports up to the configured policy limit.</p></div><Button variant="outline" size="sm">Browse</Button></article>

          <StoragePanel title="Folders" action={<Button variant="outline" size="sm"><FolderPlus size={15} />Create</Button>}>
            <div className="storage-folder-grid">{folders.map((folder) => <button className="storage-folder" type="button" key={folder.name}><span className="storage-folder-icon"><FolderPlus size={18} /></span><strong>{folder.name}</strong><p>{folder.count} files - {folder.size}</p><small>{folder.owner} - {folder.updated}</small></button>)}</div>
          </StoragePanel>

          <StoragePanel title="Files" action={<BulkActions selectedCount={selectedCount} />}>
            <div className="storage-table" role="table" aria-label="Files"><div className="storage-table-row storage-table-head" role="row"><span><CheckSquare size={15} />Name</span><span>Type</span><span>Size</span><span>Status</span><span>Updated</span><span aria-label="Actions" /></div>{files.map((file) => <div className="storage-table-row" role="row" key={file.name}><span><file.icon size={17} /><strong>{file.name}</strong></span><span>{file.type}</span><span>{file.size}</span><span><Badge variant={file.status === "Ready" ? "success" : file.status === "Review" ? "warning" : "info"}>{file.status}</Badge></span><span>{file.updated}</span><span><IconButton variant="ghost" size="sm" aria-label={`More actions for ${file.name}`}><MoreHorizontal size={16} /></IconButton></span></div>)}</div>
          </StoragePanel>
        </div>

        <aside className="storage-side-panel" aria-label="Storage details">
          <StoragePanel title="Selected asset">
            <div className="storage-preview"><SelectedIcon size={34} /><strong>{files[0].name}</strong><p>Version 3 - PDF - {files[0].size}</p></div>
            <dl className="storage-meta"><div><dt>Owner</dt><dd>{files[0].owner}</dd></div><div><dt>Status</dt><dd>Encrypted and ready</dd></div><div><dt>Provider</dt><dd>Local development</dd></div><div><dt>Path</dt><dd>/Knowledge sources/Policies</dd></div></dl>
            <div className="storage-tag-row">{files[0].tags.map((tag) => <Badge key={tag}>{tag}</Badge>)}</div>
            <div className="storage-detail-actions"><Button variant="outline" size="sm"><Download size={15} />Download</Button><Button variant="outline" size="sm"><ArchiveRestore size={15} />Restore</Button><Button variant="destructive" size="sm"><Trash2 size={15} />Delete</Button></div>
          </StoragePanel>

          <StoragePanel title="Uploads"><div className="storage-upload-list">{uploads.map((upload) => <div className="storage-upload-item" key={upload.name}><div><strong>{upload.name}</strong><p>{upload.status} - {upload.speed}</p></div><Progress value={upload.progress} /></div>)}</div></StoragePanel>

          <StoragePanel title="Recent activity"><div className="storage-activity-list">{activity.map((event) => <div className="storage-activity" key={event.title}><span>{event.time}</span><div><strong>{event.title}</strong><p>{event.detail}</p></div></div>)}</div></StoragePanel>
        </aside>
      </section>

      <section className="storage-state-grid" aria-label="Storage states">{emptyStorageStates.map((state) => <EmptyState key={state.title} title={state.title} description={state.description} action={<Button variant="outline" size="sm"><state.icon size={15} />{state.action}</Button>} />)}<div className="storage-card"><Skeleton className="storage-skeleton" /><Skeleton className="storage-skeleton-line" /><Skeleton className="storage-skeleton-line" /></div><ErrorState title="Storage provider unavailable" description="Provider failures should preserve the file manager layout and offer a clear retry path." onRetry={() => undefined} /></section>
    </div>
  );
}

function StoragePanel({ title, action, children }: { title: string; action?: React.ReactNode; children: React.ReactNode }) {
  return <article className="storage-card"><div className="storage-panel-head"><h2>{title}</h2>{action}</div>{children}</article>;
}

function BulkActions({ selectedCount }: { selectedCount: number }) {
  return <div className="storage-bulk-actions"><Badge>{selectedCount} selected</Badge><Button variant="outline" size="sm">Move</Button><Button variant="outline" size="sm">Tag</Button><Button variant="destructive" size="sm">Delete</Button></div>;
}