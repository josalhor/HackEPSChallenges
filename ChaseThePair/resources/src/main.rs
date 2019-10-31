extern crate rand;
use std::time::{Duration, Instant};
use std::thread::sleep;
use rand::prelude::*;
use std::process::{Command, Stdio};
use std::{io, env};
use std::io::Write;

type NumberPr = i16;
const MAX_GEN : u16 = u16::max_value();
const MIN_GEN : u16 = u16::min_value();


fn get_vector(mut rng: ThreadRng, len: usize) -> Vec<NumberPr> {
    (0..len).map(|_| (rng.gen_range(MIN_GEN, MAX_GEN) as NumberPr).abs()).collect()
}

fn get_vectors(len: usize) -> [Vec<NumberPr>; 2] {
    let rng = rand::thread_rng();
    [get_vector(rng, len), get_vector(rng, len)]
}

fn find_closer(vec: &Vec<NumberPr>, to_chase: NumberPr) -> NumberPr {
    assert!(vec.len() > 0);
    vec.iter()
        .min_by_key(|&i| ( to_chase - i).abs())
        .unwrap().clone()
}

fn main() {
    let to_chase = env::args().nth(1).unwrap().parse::<NumberPr>().unwrap();
    let len = env::args().nth(2).unwrap().parse::<usize>().unwrap();
    let vectors = get_vectors(len);
    let start = Instant::now();
    let values : Vec<_> = vectors.iter().map(|v| find_closer(v, to_chase)).collect();
    println!("{} ms for whatever you did.", start.elapsed().as_millis());
    println!("To chase: {:?}", to_chase);
    println!("Vectors: {:?}", vectors);
    println!("Solutions: {:?}", values);
}
