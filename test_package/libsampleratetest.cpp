#include <samplerate.h>


int main()
{
   int error;
   auto* srcResult = src_new(1, 2, &error);

   if (srcResult)
   {
      auto* delResult = src_delete(srcResult) ;
   }

   return 0;
}
