/* hit4: read packed signature records (nat bits, recbytes each) from a NEG file and a POS file;
   mark every subset of size <= K (K<=4) of the true atoms of each record; output the minimal unmarked-in-NEG sets
   that are marked-in-POS (non-vacuous): i.e. hypothesis sets H of size <= K with no negative record containing H,
   every proper subset of H contained in some negative record, and some positive record containing H.
   Usage: hit4 nat K neg.bin pos.bin  [more neg files via env? no: concatenate with cat] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int nat, K;
static uint64_t C[80][5];
static void binom(){ for(int n=0;n<80;n++){C[n][0]=1; for(int k=1;k<5;k++) C[n][k]= n>=k ? C[n-1][k-1]+C[n-1][k] : 0;} }
/* rank of a sorted k-subset (a0<a1<...) in colex order */
static inline uint64_t rank1(int a){return a;}
static inline uint64_t rank2(int a,int b){return C[b][2]+a;}
static inline uint64_t rank3(int a,int b,int c){return C[c][3]+C[b][2]+a;}
static inline uint64_t rank4(int a,int b,int c,int d){return C[d][4]+C[c][3]+C[b][2]+a;}
static uint8_t *mk[5], *mkp[5];
static void mark(uint8_t **M, int *t, int nt){
  for(int i=0;i<nt;i++){ M[1][rank1(t[i])]=1;
    if(K<2) continue;
    for(int j=i+1;j<nt;j++){ M[2][rank2(t[i],t[j])]=1;
      if(K<3) continue;
      for(int k=j+1;k<nt;k++){ M[3][rank3(t[i],t[j],t[k])]=1;
        if(K<4) continue;
        for(int l=k+1;l<nt;l++) M[4][rank4(t[i],t[j],t[k],t[l])]=1; }}}
}
static void process(const char *fn, uint8_t **M){
  FILE *f=fopen(fn,"rb"); if(!f){perror(fn); exit(1);}
  int rb=(nat+7)/8; uint8_t *buf=malloc(rb); int t[80]; long nrec=0;
  while(fread(buf,1,rb,f)==(size_t)rb){ int nt=0;
    for(int a=0;a<nat;a++) if(buf[a/8]&(0x80>>(a%8))) t[nt++]=a;   /* numpy packbits: MSB first */
    mark(M,t,nt); nrec++; }
  fclose(f); free(buf); fprintf(stderr,"%s: %ld records\n",fn,nrec);
}
int main(int argc,char**argv){
  nat=atoi(argv[1]); K=atoi(argv[2]); binom();
  for(int k=1;k<=K;k++){ uint64_t sz=C[nat][k]; mk[k]=calloc(sz,1); mkp[k]=calloc(sz,1); }
  process(argv[3],mk); process(argv[4],mkp);
  long cnt=0;
  for(int a=0;a<nat;a++){ if(!mk[1][a] && mkp[1][a]){ printf("1 %d\n",a); cnt++; } }
  if(K>=2) for(int a=0;a<nat;a++) for(int b=a+1;b<nat;b++){ uint64_t r=rank2(a,b);
    if(!mk[2][r] && mkp[2][r] && mk[1][a] && mk[1][b]){ printf("2 %d %d\n",a,b); cnt++; } }
  if(K>=3) for(int a=0;a<nat;a++) for(int b=a+1;b<nat;b++) for(int c=b+1;c<nat;c++){ uint64_t r=rank3(a,b,c);
    if(!mk[3][r] && mkp[3][r] && mk[2][rank2(a,b)] && mk[2][rank2(a,c)] && mk[2][rank2(b,c)]){ printf("3 %d %d %d\n",a,b,c); cnt++; } }
  if(K>=4) for(int a=0;a<nat;a++) for(int b=a+1;b<nat;b++) for(int c=b+1;c<nat;c++) for(int d=c+1;d<nat;d++){ uint64_t r=rank4(a,b,c,d);
    if(!mk[4][r] && mkp[4][r] && mk[3][rank3(a,b,c)] && mk[3][rank3(a,b,d)] && mk[3][rank3(a,c,d)] && mk[3][rank3(b,c,d)]){ printf("4 %d %d %d %d\n",a,b,c,d); cnt++; } }
  fprintf(stderr,"%ld minimal valid non-vacuous sets\n",cnt); return 0;
}
