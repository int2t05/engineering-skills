# Launch Monitoring

What to monitor at launch, and the error-reporting scaffolding to have in place
before deployment. Loaded by the `shipping` skill when monitoring setup is needed.

## What to monitor

```
Application metrics:
├── Error rate (total and by endpoint)
├── Response time (p50, p95, p99)
├── Request volume
├── Active users
└── Key business metrics (conversion, engagement)

Infrastructure metrics:
├── CPU and memory utilization
├── Database connection pool usage
├── Disk space
├── Network latency
└── Queue depth (if applicable)

Client metrics:
├── Core Web Vitals (LCP, INP, CLS)
├── JavaScript errors
├── API error rates from client perspective
└── Page load time
```

## Error reporting

Client-side error boundary (React) — catches render errors and reports them with
context before showing a fallback:

```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    reportError(error, {
      componentStack: info.componentStack,
      userId: getCurrentUser()?.id,
      page: window.location.pathname,
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

Server-side error middleware (Express) — logs errors with request context and
returns a generic message so internals aren't leaked to clients:

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  reportError(err, {
    method: req.method,
    url: req.url,
    userId: req.user?.id,
  });

  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' },
  });
});
```
