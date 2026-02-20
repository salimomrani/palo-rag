import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NEVER } from 'rxjs';
import { vi } from 'vitest';
import { provideMarkdown } from 'ngx-markdown';

import { Chat } from './chat';
import { RagApiService } from '../../services/rag-api.service';

describe('Chat', () => {
  let component: Chat;
  let fixture: ComponentFixture<Chat>;
  let mockApi: { streamQuery: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    mockApi = {
      streamQuery: vi.fn().mockReturnValue(NEVER),
    };

    await TestBed.configureTestingModule({
      imports: [Chat],
      providers: [provideMarkdown(), { provide: RagApiService, useValue: mockApi }],
    }).compileComponents();

    fixture = TestBed.createComponent(Chat);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show suggestion chips when conversation is empty', () => {
    const chips = fixture.nativeElement.querySelectorAll('.suggestion-chip');
    expect(chips.length).toBeGreaterThan(0);
  });

  it('should hide suggestion chips when there are messages', () => {
    component.messages.set([{ id: '1', role: 'user', content: 'hello' }]);
    fixture.detectChanges();
    const chips = fixture.nativeElement.querySelectorAll('.suggestion-chip');
    expect(chips.length).toBe(0);
  });

  it('should have canSend false when prompt is empty', () => {
    expect(component.canSend()).toBe(false);
  });

  it('should have canSend false when isLoading is true', () => {
    component.prompt.set('test');
    component.isLoading.set(true);
    expect(component.canSend()).toBe(false);
  });

  it('should call streamQuery with the prompt when sendMessage is called', () => {
    component.prompt.set('hello');
    component.sendMessage();
    expect(mockApi.streamQuery).toHaveBeenCalledWith('hello');
  });

  it('should not call streamQuery when prompt is empty', () => {
    component.prompt.set('');
    component.sendMessage();
    expect(mockApi.streamQuery).not.toHaveBeenCalled();
  });
});
