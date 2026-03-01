import { ComponentFixture, TestBed } from '@angular/core/testing';
import { vi } from 'vitest';

import { HistoryPanel } from './history-panel';
import { ConversationService } from '../../../services/conversation.service';
import { RagApiService } from '../../../services/rag-api.service';
import type { ConversationSummary } from '../../../services/rag-api.service';

describe('HistoryPanel', () => {
  let fixture: ComponentFixture<HistoryPanel>;
  let component: HistoryPanel;
  let mockApi: {
    getHistory: ReturnType<typeof vi.fn>;
    getConversation: ReturnType<typeof vi.fn>;
    deleteConversation: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    sessionStorage.clear();

    mockApi = {
      getHistory: vi.fn().mockReturnValue({ subscribe: vi.fn() }),
      getConversation: vi.fn().mockReturnValue({ subscribe: vi.fn() }),
      deleteConversation: vi.fn().mockReturnValue({ subscribe: vi.fn() }),
    };

    await TestBed.configureTestingModule({
      imports: [HistoryPanel],
      providers: [{ provide: RagApiService, useValue: mockApi }],
    }).compileComponents();

    fixture = TestBed.createComponent(HistoryPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have a loadMore() method that delegates to conversationService.loadMore()', () => {
    const convService = TestBed.inject(ConversationService);
    vi.spyOn(convService, 'loadMore').mockImplementation(() => {});

    component.loadMore();

    expect(convService.loadMore).toHaveBeenCalled();
  });

  it('should render "Charger plus" button when hasMore is true', () => {
    const convService = TestBed.inject(ConversationService);
    const summaries: ConversationSummary[] = Array.from({ length: 50 }, (_, i) => ({
      session_id: `s${i}`,
      started_at: '2026-01-01',
      first_question: `Q${i}`,
      exchange_count: 1,
    }));
    convService.conversations.set(summaries);
    convService.hasMore.set(true);
    fixture.detectChanges();

    const btn = fixture.nativeElement.querySelector('.btn-load-more');
    expect(btn).not.toBeNull();
    expect(btn.textContent.trim()).toBe('charger plus');
  });

  it('should NOT render "Charger plus" button when conversations.length < 50', () => {
    const convService = TestBed.inject(ConversationService);
    convService.conversations.set([
      { session_id: 's1', started_at: '2026-01-01', first_question: 'Q1', exchange_count: 1 },
    ]);
    fixture.detectChanges();

    const btn = fixture.nativeElement.querySelector('.btn-load-more');
    expect(btn).toBeNull();
  });
});
