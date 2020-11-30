# vaccine_rollout_sim
Simulates a rollout of a UK covid vaccination program

It allows vaccine prioritization to be experimented with to see if overall death toll can be reduced.
It simulates full and partial lockdowns based on threshold levels.

It can be given the size of the real-world population.
Internally it uses a cohort of one million randomly created people, which can be easily adjusted to improve runtime (from several hours)

A weakness of the modelling is it assumes random mixing, in the real world this is unlikely to be true, 
mixing is likely to be localised by location, age, ethinicity etc. 
It would be kind of cool to introduce placing people in tiers too to see if prioritizing higher tiers made a difference. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
