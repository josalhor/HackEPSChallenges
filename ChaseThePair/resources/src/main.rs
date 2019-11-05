extern crate rand;
extern crate rayon;

use rayon::prelude::*;
use std::time::{Instant};
use rand::prelude::*;
use std::{env};

type NumberPr = i32;
const MAX_GEN : u32 = u32::max_value();
const MIN_GEN : u32 = u32::min_value();


fn get_vector(mut rng: ThreadRng, len: usize) -> Vec<NumberPr> {
    (0..len).map(|_| (rng.gen_range(MIN_GEN, MAX_GEN) as NumberPr).abs()).collect()
}

fn get_vectors(len: usize) -> [Vec<NumberPr>; 2] {
    let rng = rand::thread_rng();
    [get_vector(rng, len), get_vector(rng, len)]
}

fn find_closer(vec: &Vec<NumberPr>, to_chase: NumberPr) -> NumberPr {
    assert!(vec.len() > 0);
    vec.par_iter()
        .min_by_key(|&i| (to_chase - i).abs()) // if the search space was small enough one could leave early by return if found 0
        .unwrap()
        .clone()
}

/*
 * Use: ./program toChase NumberElementsLen
*/

fn main() {

    let to_chase = env::args().nth(1).unwrap().parse::<NumberPr>().unwrap();
    let len = env::args().nth(2).unwrap().parse::<usize>().unwrap();
    let vectors = get_vectors(len);
    let start = Instant::now();
    let values : Vec<_> = vectors.iter().map(|v| find_closer(v, to_chase)).collect();
    println!("{} ms for whatever you did.", start.elapsed().as_millis());
    println!("To chase: {:?}", to_chase);
    //println!("Vectors: {:?}", vectors);
    println!("Solutions: {:?}", values);
}
