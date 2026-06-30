# Omnichannel Attachment Guide

Attachments are modeled through `message_attachments` and reference the Storage Platform through `storage_object_id`.

## Supported Types

Images, audio, video, documents, PDFs, forms, quick replies, lists, carousels, and interactive cards are represented as metadata and normalized payloads.

## Security

Attachments should use storage references, access policy metadata, and scan state metadata. Virus scanning and preview generation are architecture-ready but not implemented in Task 022.