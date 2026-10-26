# Mobile profile

MUST define OS/device support and exercise critical flows on representative devices or labeled emulators. Check touch/screen-reader input, lifecycle interruption, background/foreground, offline behavior, and interrupted updates as applicable.

MUST handle denied/revoked permissions, minimize device privileges, use platform-appropriate secure credential storage, and keep server secrets out of distributed apps. Verify backend authority independently of UI. Review sync conflicts, duplicate writes/retries, local migrations and cleanup where used.

MUST distinguish store submission from rollout approval. Plan staged rollout, crash/user-outcome signals and recovery, accounting for clients that cannot immediately downgrade. Maintain compatible backend behavior where needed.
