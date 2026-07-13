/**
 * Global message audit logging API tests.
 *
 * Verifies that creating and deleting global messages produces audit log
 * entries (PROJQUAY-12222).
 *
 * Covered areas:
 *  - global_message_create audit log entry with metadata
 *  - global_message_delete audit log entry with uuid metadata
 */

import {test, expect} from '../../fixtures';

// ---------------------------------------------------------------------------
// Global message create audit log
// ---------------------------------------------------------------------------
test.describe(
  'Global Message Create Audit Log',
  {tag: ['@api', '@auth:Database']},
  () => {
    test(
      'creating a global message produces a global_message_create log entry',
      {tag: '@superuser'},
      async ({superuserApi, adminClient}) => {
        // Create a global message
        const msg = await superuserApi.message(
          'Audit log test message',
          'warning',
        );

        // Query the superuser logs
        const resp = await adminClient.get('/api/v1/superuser/logs');
        expect(resp.status()).toBe(200);
        const body = await resp.json();
        expect(Array.isArray(body.logs)).toBe(true);

        // Find the global_message_create log entry
        const createEntry = body.logs.find(
          (entry: {kind: string; metadata: Record<string, unknown>}) =>
            entry.kind === 'global_message_create' &&
            entry.metadata?.content === 'Audit log test message',
        );
        expect(createEntry).toBeDefined();
        expect(createEntry.metadata.severity).toBe('warning');
        expect(createEntry.metadata.media_type).toBeDefined();
        expect(createEntry.metadata.content).toBe('Audit log test message');

        // Cleanup is automatic via superuserApi fixture
        void msg;
      },
    );
  },
);

// ---------------------------------------------------------------------------
// Global message delete audit log
// ---------------------------------------------------------------------------
test.describe(
  'Global Message Delete Audit Log',
  {tag: ['@api', '@auth:Database']},
  () => {
    test(
      'deleting a global message produces a global_message_delete log entry',
      {tag: '@superuser'},
      async ({superuserApi, adminClient}) => {
        // Create a global message (auto-cleanup disabled by manual delete below)
        const msg = await superuserApi.message(
          'Message to delete for audit',
          'info',
        );

        // Delete the message via the raw API client
        const deleteResp = await adminClient.delete(
          `/api/v1/message/${msg.uuid}`,
        );
        expect(deleteResp.status()).toBe(204);

        // Query the superuser logs
        const resp = await adminClient.get('/api/v1/superuser/logs');
        expect(resp.status()).toBe(200);
        const body = await resp.json();
        expect(Array.isArray(body.logs)).toBe(true);

        // Find the global_message_delete log entry
        const deleteEntry = body.logs.find(
          (entry: {kind: string; metadata: Record<string, unknown>}) =>
            entry.kind === 'global_message_delete' &&
            entry.metadata?.uuid === msg.uuid,
        );
        expect(deleteEntry).toBeDefined();
        expect(deleteEntry.metadata.uuid).toBe(msg.uuid);
      },
    );
  },
);
