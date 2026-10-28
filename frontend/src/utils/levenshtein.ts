export function lev(a: string, b: string): number {
  const m = [...Array(b.length + 1).keys()];
  for (let i = 1; i <= a.length; i++) {
    let p = m[0];
    m[0] = i;
    for (let j = 1; j <= b.length; j++) {
      const t = m[j];
      m[j] = Math.min(m[j] + 1, m[j - 1] + 1, p + (a[i - 1] === b[j - 1] ? 0 : 1));
      p = t;
    }
  }
  return m[b.length];
}
