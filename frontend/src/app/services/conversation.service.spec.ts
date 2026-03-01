import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { vi } from 'vitest';

import { ConversationService } from './conversation.service';
import { RagApiService } from './rag-api.service';
import type { ConversationSummary, ConversationDetail } from './rag-api.service';

describe('ConversationService', () => {
  let service: ConversationService;
  let mockApi: {
    getHistory: ReturnType<typeof vi.fn>;
    getConversation: ReturnType<typeof vi.fn>;
    deleteConversation?: ReturnType<typeof vi.fn>;
  };

  beforeEach(() => {
    sessionStorage.clear();

    mockApi = {
      getHistory: vi.fn().mockReturnValue(of([])),
      getConversation: vi.fn().mockReturnValue(of({ session_id: 'abc', exchanges: [] })),
    };

    TestBed.configureTestingModule({
      providers: [ConversationService, { provide: RagApiService, useValue: mockApi }],
    });

    service = TestBed.inject(ConversationService);
  });

  it('should generate sessionId at construction', () => {
    expect(service.sessionId).toBeTruthy();
    expect(sessionStorage.getItem('palo_session_id')).toBe(service.sessionId);
  });

  it('should reuse sessionId from sessionStorage', () => {
    const existing = 'existing-session-uuid';
    sessionStorage.setItem('palo_session_id', existing);

    TestBed.resetTestingModule();
    TestBed.configureTestingModule({
      providers: [ConversationService, { provide: RagApiService, useValue: mockApi }],
    });
    const service2 = TestBed.inject(ConversationService);

    expect(service2.sessionId).toBe(existing);
  });

  it('should call getHistory on loadHistory()', () => {
    const summaries: ConversationSummary[] = [
      {
        session_id: 's1',
        started_at: '2024-01-01T00:00:00Z',
        first_question: 'Hi',
        exchange_count: 1,
      },
    ];
    mockApi.getHistory.mockReturnValue(of(summaries));

    service.loadHistory();

    expect(mockApi.getHistory).toHaveBeenCalled();
    expect(service.conversations()).toEqual(summaries);
  });

  it('should call getConversation on loadConversation()', () => {
    const detail: ConversationDetail = { session_id: 's1', exchanges: [] };
    mockApi.getConversation.mockReturnValue(of(detail));

    service.loadConversation('s1');

    expect(mockApi.getConversation).toHaveBeenCalledWith('s1');
    expect(service.selectedConversation()).toEqual(detail);
  });

  it('should call deleteConversation and remove from conversations signal', async () => {
    const summaries: ConversationSummary[] = [
      { session_id: 's1', started_at: '2026-01-01', first_question: 'Q', exchange_count: 1 },
      { session_id: 's2', started_at: '2026-01-02', first_question: 'Q2', exchange_count: 2 },
    ];

    mockApi.deleteConversation = vi.fn().mockReturnValue(of(null));
    mockApi.getHistory = vi.fn().mockReturnValue(of(summaries));

    const service = TestBed.inject(ConversationService);
    service.conversations.set(summaries);

    service.deleteConversation('s1');

    expect(mockApi.deleteConversation).toHaveBeenCalledWith('s1');
    expect(service.conversations()).toHaveLength(1);
    expect(service.conversations()[0].session_id).toBe('s2');
  });

  it('loadMore() should append results to existing conversations', () => {
    const first: ConversationSummary[] = [
      { session_id: 's1', started_at: '2026-01-01', first_question: 'Q1', exchange_count: 1 },
    ];
    const more: ConversationSummary[] = [
      { session_id: 's2', started_at: '2026-01-02', first_question: 'Q2', exchange_count: 2 },
    ];

    service.conversations.set(first);
    mockApi.getHistory.mockReturnValue(of(more));

    service.loadMore();

    expect(service.conversations()).toEqual([...first, ...more]);
  });

  it('loadMore() should call getHistory with incremented offset', () => {
    mockApi.getHistory.mockReturnValue(of([]));

    service.loadMore();

    expect(mockApi.getHistory).toHaveBeenCalledWith(50, 50);
  });

  it('loadHistory() should reset offset to 0', () => {
    mockApi.getHistory.mockReturnValue(of([]));

    service.loadMore();
    service.loadHistory();

    expect(mockApi.getHistory).toHaveBeenLastCalledWith(50, 0);
  });
});
