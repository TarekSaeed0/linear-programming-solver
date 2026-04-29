import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Problem } from '../models/problem';
import { Solution } from '../models/solution';
import { MethodName } from '../models/method';

export interface SolveRequest {
  method: MethodName;
  problem: Problem;
}

@Injectable({
  providedIn: 'root',
})
export class SolverService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/solve/';

  solve(method: MethodName, problem: Problem): Observable<Solution> {
    const requestPayload: SolveRequest = { method, problem };
    return this.http.post<Solution>(this.apiUrl, requestPayload);
  }
}
